# Conference GenJS Few-Shot

## Contents

1. Purpose
2. What was preserved
3. What was stripped
4. How to use it inside this skill
5. Pattern inventory
6. Code reference

## 1. Purpose

This reference captures the most reusable helper-layer patterns from the repository's meeting-type direct `pptxgenjs` workflow and rewrites them as a sanitized conference-style scaffold.

Read it when you need:

- a concrete few-shot for a classical conference serif treatment;
- a stable footer/title/tag hierarchy for an academic talk;
- a worked example of figure-dominant result slides, takeaway bars, and compact metric cards;
- a reminder of how complete English speaker notes were attached in the older script-first workflow.

Do **not** use this file to change the production route of `pptx-skill`. The default route remains:

`HTML/Tailwind -> PptxGenJS export`

Treat this as a composition and helper reference, not as a second implementation contract.

## 2. What Was Preserved

The few-shot keeps the parts that were broadly reusable across conference-style academic decks:

- a dark footer band with title, date, and page number;
- a one-line slide title plus thin horizontal rule;
- a top-right section tag for quick orientation;
- a result page with one dominant figure and a row of compact metric cards;
- a takeaway bar near the bottom of the slide;
- a close slide built from a few conclusion tiles rather than dense bullets;
- explicit speaker notes for every slide.

## 3. What Was Stripped

The few-shot removes all meeting-specific identifiers and unpublished content:

- paper titles and method names;
- presenter, coauthor, institution, and venue names;
- real dates and file names;
- original figure identifiers;
- workload names, benchmark names, and exact measured values.

Replace placeholders such as `[Paper Title]`, `[Metric A]`, and `[Institution]` only with user-approved, source-grounded content.

## 4. How To Use It Inside This Skill

Because this skill authors slides in HTML first, use the GenJS template as a translation reference:

| GenJS helper | HTML/Tailwind analogue | Why it matters |
|---|---|---|
| `addFooter` | footer band component | keeps orientation stable without crowding the body |
| `addTitle` | title row plus rule | gives conference slides a crisp top anchor |
| `addSectionTag` | upper-right metadata label | helps long talks without a separate agenda slide |
| `addFigure` | dominant figure block | protects aspect ratio and evidence priority |
| `metricCard` | compact metric strip | turns one result into 2-3 memorable numbers |
| `addTakeaway` | bottom takeaway line | forces one sentence per slide |
| `addConclusionTile` | close-slide synthesis blocks | keeps the ending analytical rather than ornamental |

When adapting the pattern, preserve hierarchy and restraint. Do not blindly copy serif type, dark footer, or navy accents into every academic deck. Match the active visual family in [design.md](design.md).

## 5. Pattern Inventory

### Cover

Use a dark top field, short title, one-line subtitle, presenter line, and institution line. Keep the slide minimal.

### Result-dominant page

Use one wide figure across the center, then 2-3 metric cards, then a takeaway sentence. This is the strongest reusable pattern from the original meeting deck.

### Close page

Use 3-5 conclusion tiles plus one final answer sentence. Add `Thanks & Q&A` only as secondary metadata.

### Notes discipline

Attach speaker notes as complete audience-facing prose, not as TODO items or slide-construction comments.

## 6. Code Reference

The sanitized code scaffold lives here:

- [conference-genjs-core-template.cjs](conference-genjs-core-template.cjs)

Copy from it only when a direct-script example is genuinely useful for reasoning about hierarchy, geometry, or notes. Keep the live skill workflow and QA gates unchanged.

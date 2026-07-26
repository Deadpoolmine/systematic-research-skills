# Quality Checklist

Run every applicable check. Do not deliver on the strength of browser preview alone.

## 1. Content And Evidence

- [ ] The communication job, audience, duration, language, and source boundary are recorded.
- [ ] Every main-deck slide has one narrative job and one primary claim.
- [ ] Every result supports a stated question, conclusion, or contribution.
- [ ] Every non-trivial claim, number, chart, table, quote, and external visual maps to the evidence ledger.
- [ ] Units, denominators, baselines, uncertainty, sample sizes, and qualifiers match the source.
- [ ] Planned, preliminary, and observed results are labeled correctly.
- [ ] No `[SOURCE NEEDED]`, draft note, prompt text, or unresolved placeholder remains.
- [ ] Limitations and scope boundaries are stated honestly.
- [ ] Reusable examples contain no real personal, institutional, unpublished, or project-specific identifiers.

## 2. Narrative And Copy

- [ ] The opening establishes a real question, gap, or stake.
- [ ] Slide order is cumulative rather than a paper-section inventory.
- [ ] Titles state takeaways where evidence permits.
- [ ] Visible copy is audience-facing and does not expose timings, talk tracks, or implementation instructions.
- [ ] Repetition and non-essential background have been removed.
- [ ] The closing answers the opening question and does not end on an unframed detail.
- [ ] The timed main sequence fits the speaking slot with contingency.

## 3. Browser Render

- [ ] Every `slide-N.js` appears in the preview in the correct order.
- [ ] Every page has a 1440 x 810 root and consistent safe margins.
- [ ] No title wraps unexpectedly.
- [ ] No text, image, chart, equation, footer, or page number is clipped.
- [ ] No unintended overlap appears at full size.
- [ ] Text contrast and hierarchy are readable under projection conditions.
- [ ] Figure axes, legends, units, panel labels, and annotations remain legible.
- [ ] Images preserve aspect ratio and intended crop.
- [ ] Adjacent slide silhouettes vary enough to maintain orientation without breaking consistency.
- [ ] A contact sheet confirms coherent pacing, palette, and density.
- [ ] `browser-audit.json` contains no broken image, clipped text, or out-of-bounds text issue.
- [ ] Page-role image/text allocation matches `layout-system.md`; no filler was added merely to hit a ratio.

## 4. PPTX Export

- [ ] `artifacts/presentation.pptx` exists, is non-empty, and opens successfully.
- [ ] Slide count and order match the plan.
- [ ] Every slide is rendered from the PPTX to PNG and inspected individually.
- [ ] A PPTX montage is inspected for deck-level consistency.
- [ ] Browser and PowerPoint renders are compared for line breaks, fonts, images, and color.
- [ ] All unintended overlap, clipping, and overflow warnings are fixed.
- [ ] Fonts available on the delivery machine are used or a substitution test is completed.
- [ ] Charts and tables in the PPTX still match the verified source values.
- [ ] Hyperlinks, equations, special characters, and image transparency render as intended.
- [ ] The PPTX contains editable objects where the converter supports them; no slide is silently flattened to a screenshot.
- [ ] `audit-pptx.cjs` completed and its JSON report was reviewed.
- [ ] No shape with audience-facing content extends outside the slide canvas.
- [ ] Global font-size findings are reconciled with the role-specific minimums in `design.md`; citations are not mistaken for body copy.
- [ ] Slides above 78% object coverage or below 28% object coverage are manually justified or redesigned.

When the presentations runtime is available, use its `render_slides.py`, `create_montage.py`, and `slides_test.py` helpers for PPTX-level validation. Otherwise, render with LibreOffice or PowerPoint and inspect the resulting images manually.

The coverage thresholds are review triggers, not aesthetic targets. Covers, section dividers, and intentional full-bleed scientific images may legitimately fall outside them.

## 5. Notes And Delivery

- [ ] The sidecar notes use the same slide numbering and titles as the final deck.
- [ ] When notes are part of delivery, `verify-speaker-notes.cjs` was run and its timing output was reviewed.
- [ ] External claims and assets have `[Sources]` blocks with stable evidence IDs.
- [ ] Speaker timing totals fit the slot.
- [ ] English-only notes contain no unintended CJK spillover.
- [ ] Q&A answers do not overclaim beyond verified evidence.
- [ ] Final deliverables contain no temporary builds, logs, screenshots, or confidential source files unless requested.
- [ ] The handoff states page count, language, source basis, QA performed, and unresolved limitations.

When a user says the deck does not feel close enough to a provided reference or venue style, reopen the reference and compare hierarchy, footer treatment, figure density, and spacing deliberately. Change the source HTML and layout logic rather than only nudging margins.

# Evidence And Citations

## Contents

1. Evidence ledger
2. Claim discipline
3. Figures, tables, and equations
4. Citation system
5. Privacy and anonymization

## 1. Evidence Ledger

Build the ledger before writing the slide plan. Use one row per claim, result, figure, table, or external visual.

| Field | Meaning |
|---|---|
| ID | Stable identifier such as `E03`, `F02`, or `T01` |
| Item | Exact claim, metric, figure, table, quote, or definition |
| Source | File, DOI, URL, or user-provided artifact |
| Locator | Page, section, figure, table, equation, or row/column |
| Exact value | Value and unit as reported, including uncertainty |
| Transformation | Crop, redraw, aggregation, normalization, translation, or none |
| Intended slide | Slide number or backup |
| Status | Verified, source needed, excluded, or ambiguous |

For user-supplied manuscripts, cite the exact internal locator even if the public bibliography is not yet finalized.

## 2. Claim Discipline

- Distinguish observation, interpretation, mechanism, and speculation.
- Preserve qualifiers such as preliminary, associated with, under the tested setting, and statistically non-significant.
- Never turn correlation into causation or a subset result into a universal claim.
- Never calculate an unreported percentage, average, or improvement without recording the formula and inputs.
- When rounding, keep enough precision to preserve the conclusion and use the same rounding rule across slides.
- Mark unresolved values as `[SOURCE NEEDED]`; do not display the marker in a delivered slide.
- Use neutral placeholders for missing examples. Do not invent participant quotations, reviewer comments, institutions, datasets, or outcomes.

## 3. Figures, Tables, And Equations

### Figures

- Prefer original author exports in PDF, SVG, or high-resolution PNG.
- Keep axes, legends, units, uncertainty marks, scale bars, and panel labels visible.
- Do not crop away a condition that changes interpretation.
- If simplifying a multi-panel figure, state which panels were retained and why in the ledger.
- Verify colors remain distinguishable in projection and grayscale when print handouts matter.
- Add a concise annotation only when it helps the audience see the stated finding; do not cover data.

### Redrawn Charts

Redraw only from available data. Verify:

1. category order;
2. baseline and denominator;
3. axis limits and whether zero is included;
4. units and transformations;
5. error-bar definition;
6. sample size;
7. highlighted values against the source.

Do not use a decorative chart when the numbers are unavailable.

### Tables

Show only the rows and columns needed for the slide's claim. Preserve the full table in backup when needed. Highlight the comparison cell, not the entire table. Use consistent decimal precision and explain arrows, boldface, and significance markers.

### Equations

Use a rendered equation image or MathML-compatible workflow when possible. Define every symbol needed by the audience. Use color sparingly to connect terms to a diagram or result. Never split a mathematical expression across lines merely to fit a layout.

## 4. Citation System

Use short visible citations and complete sidecar notes.

### On-Slide Form

- User paper: `Source: manuscript, Fig. 3` or `[F03]`.
- External paper: `Author et al., Year` or `[S04]`.
- Dataset or software: official name and version when relevant.
- Adapted figure: `Adapted from Author et al., Year`.

Place citations in a consistent footer zone. A citation must remain readable in the rendered PPTX; do not shrink it below the design minimum.

### Speaker-Notes Source Block

For every slide with external evidence, add:

```text
[Sources]
- [S04] Full citation or URL; accessed YYYY-MM-DD; supports the comparison claim.
- [F03] User manuscript, Figure 3; cropped to panels A and C; values unchanged.
```

Use stable IDs matching the evidence ledger. Never cite a search-result snippet when the primary source is available.

### Reference Appendix

Add one or more reference slides when citations are numerous or formally required. Keep visible short citations on evidence slides; the appendix does not replace local traceability.

## 5. Privacy And Anonymization

Reusable Skill content and examples must not contain real:

- paper titles or unpublished project names;
- author, student, advisor, reviewer, or committee names;
- school, laboratory, employer, grant, or client identifiers;
- student numbers, email addresses, phone numbers, or account IDs;
- confidential datasets, exact unreleased results, or distinctive quotations.

Use consistent placeholders: `[Paper Title]`, `[Presenter Name]`, `[Advisor Name]`, `[Institution]`, `[Lab]`, `[Dataset X]`, `[Method A]`, `[Metric]`, `[Value]`, and `[Date]`. When anonymizing a real example, replace linked details together so the remaining combination cannot identify the source.

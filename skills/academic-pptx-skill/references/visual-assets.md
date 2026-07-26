# Academic Visual Assets

## Contents

1. Source priority
2. Figures and charts
3. Tables and equations
4. Images
5. Icons
6. Preparation and verification

## 1. Source Priority

Use visual sources in this order:

1. Author-provided vector export or original plotting output.
2. High-resolution raster exported from the source PDF at 4x-5x scale.
3. A verified chart redraw from available data.
4. A focused screenshot from the source PDF when faithful table or equation reconstruction is riskier.
5. A restrained explanatory diagram created for the talk.

Never use a low-resolution screenshot when the original PDF or plotting artifact is available. Never copy an example asset from this Skill into a real deck unless it is an intentionally generic bundled asset.

## 2. Figures And Charts

- Make the figure the dominant object when it is the evidence.
- Preserve aspect ratio with `object-contain` by default.
- Crop only blank margins, captions already replaced on the slide, or unrelated panels recorded in the evidence ledger.
- Keep axes, legends, panel labels, units, uncertainty, and baseline semantics visible.
- Use direct annotations to reduce legend lookup, but do not cover data.
- Keep method/cohort colors stable across the deck.
- For a wide multi-panel figure, use a full-width band or split it into evidence-preserving panels across slides.
- Use a border only when the figure edge disappears into the slide or adjacent figures require separation.

For source-PDF crops, render at 4x-5x, crop with 20-32 px white padding, flatten transparency to white when appropriate, and verify the crop at the final projected size.

## 3. Tables And Equations

Use a table for exact lookup and a chart for patterns. Avoid showing both for the same evidence without a specific reason.

- For a table, retain only the rows and columns used by the claim.
- Use a source-PDF crop when exact formatting, symbols, or cell relationships are difficult to reproduce faithfully.
- Use a native HTML table when editability and selective highlighting matter and every value is verified.
- Use consistent precision, unit placement, and significance notation.
- Render equations with a math-capable pipeline or a high-resolution transparent image.
- Define symbols next to the equation; do not make the audience decode manuscript notation unaided.

## 4. Images

Use real images only when they reveal the study object, apparatus, sample, site, workflow, or qualitative evidence. Avoid generic stock photography, atmospheric backgrounds, or decorative technology imagery.

- Use `object-contain` for apparatus, microscopy, maps, and screenshots unless a crop is scientifically harmless.
- Use `object-cover` only for non-evidence imagery and verify the crop.
- Add scale, orientation, time, location, or sample labels when interpretation needs them.
- For qualitative examples, include enough surrounding context to avoid cherry-picking.
- Do not place essential copy inside a background image.

## 5. Icons

Icons are optional semantic aids, not decoration.

- Use icons for recurring concepts such as dataset, method, validation, risk, time, or limitation only when they improve scanning.
- Prefer a consistent open-source set such as Lucide. Save each used icon as an SVG or high-resolution PNG in the deck workspace and record its source/license.
- Do not use icon-font glyphs, emoji, platform-dependent symbols, or mixed icon families.
- Use one icon per conceptual group at most.
- Keep icon size around 24-36 px beside text and 40-56 px for a standalone stage marker.
- Use the primary or neutral color; reserve warning color for actual risk or failure.
- Pair unfamiliar icons with a text label. An icon must never carry the only meaning.

## 6. Preparation And Verification

For every visual asset, record:

```text
ID: [F03]
Source: [file/URL and locator]
Type: [original / crop / redraw / diagram / icon]
Transformation: [crop coordinates, scaling, recolor, labels added]
Integrity check: [axes, units, values, aspect ratio, license]
Intended slide: [N]
```

Before delivery:

- inspect the asset at full slide size, not only in a contact sheet;
- verify no broken path or zero-size image exists in `browser-audit.json`;
- compare the browser and rendered PPTX versions;
- confirm that crop, transparency, and font substitution did not remove scientific meaning;
- confirm that citations and licenses are present where required.

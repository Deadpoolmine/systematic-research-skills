---
name: academic-pptx-skill
description: Create and revise evidence-led academic presentations through an HTML/Tailwind authoring surface and PptxGenJS export. Use for conference talks, seminar presentations, research briefings, thesis or dissertation defenses, proposal defenses, paper-to-slides conversion, academic figures and tables, speaker notes, citations, and PPTX visual QA. Keep the workflow academic-only; do not use it for commercial pitches, marketing decks, or PowerPoint COM template inheritance.
---

# Academic PPTX

Create editable academic PPTX decks with one implementation route:

`source materials -> evidence ledger -> slide narrative -> HTML/Tailwind -> PptxGenJS -> rendered QA`

Do not switch to PowerPoint COM, VBA, `python-pptx`, screenshot-only slides, or a different presentation engine. A user-provided visual reference may influence design, but this Skill does not inherit a source PPTX master.

## Read The Required References

Before authoring slides, read:

- [academic-workflow.md](references/academic-workflow.md) for conference-talk and defense structures.
- [evidence-and-citations.md](references/evidence-and-citations.md) for claim, figure, citation, and anonymization rules.
- [design.md](references/design.md) for the academic visual system and slide geometry.
- [layout-system.md](references/layout-system.md) for page-role templates, density, and image-to-text allocation.
- [visual-assets.md](references/visual-assets.md) for figures, tables, equations, icons, and image preparation.
- [quality-checklist.md](references/quality-checklist.md) before preview, export, and delivery.

Read [speaker-notes.md](references/speaker-notes.md) when a talk script, timing plan, Q&A preparation, or source notes are needed. Read [templates/index.md](references/templates/index.md) only when selecting a bundled starting layout.
Read [conference-genjs-few-shot.md](references/conference-genjs-few-shot.md) when a user wants a classical conference-style treatment or when you need a sanitized helper-level few-shot extracted from the repository's meeting-type direct-script workflow. Use it as a composition reference only; keep the implementation route HTML/Tailwind-first.

## Non-Negotiable Rules

- Ground every non-trivial claim, value, chart, and quoted sentence in supplied or verifiable sources. Never invent missing results.
- Preserve scientific meaning. Do not change denominators, units, confidence intervals, baselines, axes, sample sizes, or qualifiers for visual convenience.
- Remove personal and paper-specific details when creating reusable examples. Use placeholders such as `[Presenter Name]`, `[Institution]`, `[Method A]`, and `[Dataset X]`.
- Give each slide one narrative job and one primary claim. Use takeaway titles instead of topic labels when evidence supports them.
- Prefer one composition on the canvas. Avoid dashboard grids, decorative card collections, pills, fake controls, marketing slogans, and ornamental technology effects.
- Use real research figures, data visualizations, equations, or restrained diagrams when they carry evidence. Never decorate a slide with an unrelated stock image.
- Keep planning notes, timing cues, prompts, and implementation language out of audience-facing slide copy.
- Include a `[Sources]` block in the sidecar speaker notes for every external asset and non-trivial external claim.

## Working Directories

Treat these as path variables:

- `SKILL_DIR`: this `academic-pptx-skill` directory.
- `WORKSPACE_DIR`: a writable project directory for one deck.

The scaffold creates:

```text
WORKSPACE_DIR/
|-- docs/
|   |-- project.json
|   `-- work/
|-- frontend/
|   |-- public/assets/images/
|   `-- src/slides/slide-N.js
`-- artifacts/
```

Keep temporary research notes, evidence ledgers, slide plans, and QA logs under `WORKSPACE_DIR/docs/work/`. Use `.txt` for generated working files. Put only final PPTX and requested handoff files in `artifacts/`.

## Environment Requirements

Use Node.js 20.19 or newer with `npm` or `pnpm`. The exporter and screenshot tool prefer an installed Chrome browser on Windows and macOS. Override browser discovery with `PPTX_BROWSER_EXECUTABLE` or `PPTX_BROWSER_CHANNEL`. On a machine without Chrome, install Playwright Chromium from `SKILL_DIR/scripts/export` with the selected package manager before exporting.

## End-To-End Workflow

### 1. Frame The Academic Communication Job

Determine the format, audience, duration, language, source boundary, and expected decision or understanding. Express the job in one sentence:

> By the end, `[audience]` should understand or accept `[outcome]` because `[central evidence-led takeaway]`.

If details are missing, use conservative defaults from `academic-workflow.md` and record the assumptions in the working notes.

### 2. Inspect Sources And Build An Evidence Ledger

Read all supplied papers, manuscripts, reports, figures, tables, and reference decks. Extract claims and assets into an evidence ledger before outlining. Record exact source locations and transformations. Mark gaps as `[SOURCE NEEDED]`; do not fill them from intuition.

### 3. Plan The Narrative

Choose the conference-talk or defense arc from `academic-workflow.md`. Create a page-by-page plan containing:

- slide number and narrative role;
- takeaway title;
- evidence IDs used;
- intended visual;
- audience-visible copy budget;
- speaking time;
- transition from the previous slide.

Remove repeated background, method inventory, and low-value detail. Put backup analyses, derivations, and extra tables in an appendix.

### 4. Define The Visual System

Use `academic-light` unless a technical dark treatment is appropriate to the field and room. Set palette, type, spacing, figure treatment, citation footer, page marker, and the page-role geometry before writing individual slides. Follow `design.md` and `layout-system.md`; user-supplied brand or institutional rules override their defaults.

### 5. Initialize The Workspace

Run once:

```bash
node "<SKILL_DIR>/scripts/setup.js" "<SKILL_DIR>" "<WORKSPACE_DIR>"
```

The command copies `assets/frontend`, installs frontend and export dependencies, and creates the academic project manifest. Do not edit files under `SKILL_DIR` while producing a deck; edit the scaffolded workspace.

### 6. Prepare Visual Evidence

Copy approved figures and images to `frontend/public/assets/images/`. Prepare them with `visual-assets.md`. Prefer the author's original vector or high-resolution raster output. Recreate a chart only when the underlying data is available and verify every value against the source. Use simple native HTML shapes only for explanatory structure, not for scientific imagery.

### 7. Author Slides

Create one file per page at `frontend/src/slides/slide-N.js`:

```javascript
window.slideDataMap.set(1, `
  <div class="w-[1440px] h-[810px] bg-white px-[88px] py-[64px]">
    <h1 class="text-[44px] leading-tight font-bold text-primary">The takeaway title</h1>
    <p class="mt-[32px] text-[26px] leading-[1.45] text-gray-700">Audience-facing evidence.</p>
  </div>
`);
```

Observe this coding contract:

- Use exactly one 1440 x 810 root element per slide.
- Use continuous numbering beginning at 1.
- Keep all visible elements inside the slide bounds with stable pixel dimensions.
- Use valid semantic HTML. Wrap text in `p`, heading, list, table, or figure elements.
- Prefer Tailwind utility classes and simple inline CSS. Avoid CSS animation, filters, blend modes, pseudo-elements, nested transforms, and effects that do not convert reliably.
- Use `object-contain` for scientific figures unless an intentional crop is verified.
- Keep citations visible but subordinate. Do not place evidence-critical text below the legibility threshold in `design.md`.
- Shorten copy or change layout before shrinking fonts.

Use bundled templates as structural starting points, then replace every placeholder and verify fit. Do not mix the light and technical-dark systems within one deck except for a deliberate section break.

### 8. Preview And Capture Every Slide

Start the local server:

```bash
cd "<WORKSPACE_DIR>/frontend"
npm run dev
```

Use `pnpm run dev` when `npm` is unavailable. The setup and export scripts detect either package manager automatically.

Capture every page while the server is running:

```bash
node "<SKILL_DIR>/scripts/screenshot-ppt.js" --url http://localhost:5173 --output "<WORKSPACE_DIR>/artifacts/html-render"
```

The capture command writes `browser-audit.json`. Add `--strict` after the first complete draft so clipping, broken images, and out-of-bounds text fail the check. Inspect every full-size PNG, then create a contact sheet:

```bash
node "<SKILL_DIR>/scripts/make-contact-sheet.js" "<WORKSPACE_DIR>/artifacts/html-render" "<WORKSPACE_DIR>/artifacts/html-contact-sheet.png"
```

Fix clipping, unexpected wrapping, low contrast, inconsistent margins, unreadable axes, broken image paths, and accidental overlap.

### 9. Export Through PptxGenJS

Run:

```bash
node "<SKILL_DIR>/scripts/export-ppt.js" "<SKILL_DIR>" "<WORKSPACE_DIR>"
```

This compiles the HTML slides, inlines Tailwind styles, and calls the bundled PptxGenJS converter. The result is `WORKSPACE_DIR/artifacts/presentation.pptx`.

### 10. Render And Validate The PPTX

Render every exported PPTX slide to PNG. Inspect the individual pages and a montage; the browser screenshots are not sufficient because browser and PowerPoint rendering can differ. Run an overflow check when the environment provides one. Follow every item in `quality-checklist.md` and re-export after any fix.

Run the bundled OOXML audit before delivery:

```bash
node "<SKILL_DIR>/scripts/audit-pptx.cjs" "<WORKSPACE_DIR>/artifacts/presentation.pptx" --json "<WORKSPACE_DIR>/artifacts/pptx-audit.json"
```

Treat the audit as a structural gate, not a substitute for rendered inspection. Review every reported low-font, out-of-bounds, unusually sparse, or unusually dense slide.

If `artifacts/speaker-notes.txt` is part of the deliverable, verify it too:

```bash
node "<SKILL_DIR>/scripts/verify-speaker-notes.cjs" "<WORKSPACE_DIR>/artifacts/speaker-notes.txt"
```

### 11. Deliver

Deliver:

- `presentation.pptx`;
- a sidecar speaker-notes file when requested or when sources were researched;
- a source/evidence ledger when the user needs auditability;
- no scratch screenshots or temporary build folders unless requested.

State the deck type, page count, language, source basis, and verification performed. Explicitly disclose unresolved source gaps or render limitations.

## Revision Workflow

For user-requested changes, update the evidence ledger and page plan first when claims or structure change. Modify only affected `slide-N.js` files, recapture all pages that could be influenced by shared styles, re-export, and rerun PPTX-level QA. Never patch the final PPTX manually through PowerPoint COM.

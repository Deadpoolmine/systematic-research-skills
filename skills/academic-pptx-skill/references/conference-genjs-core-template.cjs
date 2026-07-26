/*
 * Few-shot reference extracted and generalized from the meeting-type
 * direct PptxGenJS workflow in this repository.
 *
 * Use this file as a composition and helper-layer reference when a user
 * wants a classical conference-style academic deck with:
 * - serif typography
 * - a strong footer band
 * - figure-dominant result slides
 * - takeaway bars and compact metric cards
 * - complete speaker notes
 *
 * Keep all placeholders generic. Do not reintroduce paper titles, author
 * names, institution names, dates, figure IDs, or unpublished numbers from
 * historical decks.
 *
 * In `pptx-skill`, the production route still stays:
 *   HTML/Tailwind -> PptxGenJS export
 * This file is a few-shot reference, not a second default workflow.
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

function addBundledNodePaths() {
  const base =
    process.env.CODEX_NODE_MODULES ||
    path.join(
      os.homedir(),
      ".cache",
      "codex-runtimes",
      "codex-primary-runtime",
      "dependencies",
      "node",
      "node_modules",
    );
  const Module = require("module");
  const extra = [base];
  const pnpm = path.join(base, ".pnpm");
  if (fs.existsSync(pnpm)) {
    for (const entry of fs.readdirSync(pnpm, { withFileTypes: true })) {
      if (entry.isDirectory()) extra.push(path.join(pnpm, entry.name, "node_modules"));
    }
  }
  process.env.NODE_PATH = [process.env.NODE_PATH, ...extra].filter(Boolean).join(path.delimiter);
  Module._initPaths();
}

addBundledNodePaths();
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "[Presenter Name]";
pptx.company = "[Institution]";
pptx.subject = "[Research Area] conference presentation";
pptx.title = "[Paper Title]";
pptx.lang = "en-US";
pptx.theme = {
  headFontFace: "Times New Roman",
  bodyFontFace: "Times New Roman",
  lang: "en-US",
};

const W = 13.333;
const FONT = "Times New Roman";
const ROOT = process.cwd();
const FIG_DIR = path.join(ROOT, "assets", "paper_figures_hq");
const LOGO = path.join(ROOT, "conference-logo.png");
const OUT = path.join(ROOT, "Academic_Conference_FewShot.pptx");
const FOOTER_TITLE = "[Paper Title]";
const DATE = "[Month YYYY]";

const C = {
  blue: "0B4F8A",
  deep: "073763",
  line: "173B5F",
  grid: "2E5577",
  red: "C00000",
  text: "111111",
  muted: "555555",
  white: "FFFFFF",
  orange: "D97706",
  green: "2B8A57",
  paleBlue: "F8FBFF",
  paleGreen: "F8FFF9",
  paleOrange: "FFF9F0",
};

function fig(name) {
  return path.join(FIG_DIR, `${name}.png`);
}

function addFooter(slide, pageIndex, opts = {}) {
  const showLogo = opts.logo !== false && fs.existsSync(LOGO);
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 6.78,
    w: W,
    h: 0.59,
    fill: { color: C.deep },
    line: { color: C.deep },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 7.37,
    w: W,
    h: 0.13,
    fill: { color: "1E9BD7" },
    line: { color: "1E9BD7" },
  });
  if (showLogo) {
    slide.addImage({ path: LOGO, x: 0.04, y: 6.72, w: 0.93, h: 0.70 });
  }
  slide.addText(FOOTER_TITLE, {
    x: showLogo ? 1.16 : 0.50,
    y: 6.94,
    w: showLogo ? 8.72 : 9.34,
    h: 0.32,
    fontFace: FONT,
    fontSize: 16.2,
    bold: true,
    color: C.white,
    margin: 0,
    fit: "shrink",
    wrap: false,
    breakLine: false,
    valign: "mid",
  });
  slide.addText(DATE, {
    x: 9.92,
    y: 6.94,
    w: 1.75,
    h: 0.32,
    fontFace: FONT,
    fontSize: 16.0,
    color: C.white,
    margin: 0,
    align: "right",
  });
  slide.addText(String(pageIndex), {
    x: 12.18,
    y: 6.94,
    w: 0.86,
    h: 0.32,
    fontFace: FONT,
    fontSize: 16.0,
    color: C.white,
    margin: 0,
    align: "right",
  });
}

function addTitle(slide, title) {
  slide.addText(title, {
    x: 0.42,
    y: 0.18,
    w: 8.86,
    h: 0.34,
    fontFace: FONT,
    fontSize: title.length > 44 ? 24.0 : 27.5,
    bold: true,
    color: C.deep,
    margin: 0,
    fit: "shrink",
    wrap: false,
    breakLine: false,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 0.42,
    y: 0.82,
    w: 12.10,
    h: 0,
    line: { color: C.line, width: 2.05 },
  });
}

function addSectionTag(slide, tag) {
  slide.addText(tag, {
    x: 9.60,
    y: 0.23,
    w: 2.92,
    h: 0.20,
    fontFace: FONT,
    fontSize: 18.8,
    bold: true,
    color: C.deep,
    align: "right",
    margin: 0,
    fit: "shrink",
    wrap: false,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 10.00,
    y: 0.56,
    w: 2.52,
    h: 0,
    line: { color: C.blue, width: 2.15 },
  });
}

function addBullets(slide, items, x, y, w, h, opts = {}) {
  const runs = [];
  for (const item of items) {
    if (Array.isArray(item)) {
      item.forEach((part, index) => {
        runs.push({
          text: `${index === 0 ? "• " : ""}${part.text}`,
          options: {
            bold: !!part.bold,
            color: part.color || C.text,
            breakLine: index === item.length - 1,
          },
        });
      });
    } else {
      runs.push({
        text: `• ${item}`,
        options: { breakLine: true, color: C.text },
      });
    }
  }
  slide.addText(runs, {
    x,
    y,
    w,
    h,
    fontFace: FONT,
    fontSize: opts.fontSize || 23,
    color: C.text,
    margin: 0,
    fit: "shrink",
    paraSpaceAfter: opts.spaceAfter ?? 12,
    paraSpaceAfterPt: opts.spaceAfter ?? 12,
    lineSpacingMultiple: opts.lineSpacingMultiple || 1.18,
    breakLine: false,
  });
}

function addFigure(slide, name, x, y, w, h, opts = {}) {
  const imagePath = fig(name);
  const frame = opts.frame === true;
  const pad = opts.pad ?? (frame ? 0.04 : 0);
  if (frame) {
    slide.addShape(pptx.ShapeType.rect, {
      x,
      y,
      w,
      h,
      fill: { color: C.white },
      line: { color: opts.line || C.line, width: 1.65 },
    });
  }
  if (fs.existsSync(imagePath)) {
    slide.addImage({
      path: imagePath,
      x: x + pad,
      y: y + pad,
      w: w - 2 * pad,
      h: h - 2 * pad,
      sizing: {
        type: "contain",
        x: x + pad,
        y: y + pad,
        w: w - 2 * pad,
        h: h - 2 * pad,
      },
    });
  } else {
    slide.addText(`[Missing figure: ${name}]`, {
      x,
      y,
      w,
      h: 0.30,
      fontFace: FONT,
      fontSize: 18,
      color: C.red,
      margin: 0,
    });
  }
}

function addTakeaway(slide, text, y = 6.12) {
  slide.addShape(pptx.ShapeType.line, {
    x: 0.54,
    y: y - 0.14,
    w: 12.22,
    h: 0,
    line: { color: C.line, width: 1.65 },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 0.54,
    y: y - 0.14,
    w: 1.22,
    h: 0,
    line: { color: C.red, width: 2.80 },
  });
  slide.addText("Takeaway:", {
    x: 0.72,
    y,
    w: 1.76,
    h: 0.22,
    fontFace: FONT,
    fontSize: 23.2,
    bold: true,
    color: C.red,
    margin: 0,
    fit: "shrink",
    wrap: false,
    breakLine: false,
  });
  slide.addText(text, {
    x: 2.46,
    y,
    w: 10.06,
    h: 0.22,
    fontFace: FONT,
    fontSize: 22.4,
    bold: true,
    color: C.deep,
    margin: 0,
    fit: "shrink",
    wrap: false,
    breakLine: false,
  });
}

function metricCard(slide, main, label, x, y, w, h, color = C.blue, fill = C.white, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x,
    y,
    w,
    h,
    fill: { color: fill },
    line: { color, width: opts.lineWidth || 1.9 },
  });
  slide.addText(main, {
    x: x + 0.18,
    y: y + (opts.mainY ?? 0.12),
    w: w - 0.36,
    h: opts.mainH ?? 0.36,
    fontFace: FONT,
    fontSize: opts.mainSize || 30,
    bold: true,
    color,
    align: "center",
    margin: 0,
    fit: "shrink",
  });
  slide.addText(label, {
    x: x + 0.18,
    y: y + (opts.labelY ?? 0.58),
    w: w - 0.36,
    h: h - (opts.labelBottom ?? 0.66),
    fontFace: FONT,
    fontSize: opts.labelSize || 18.2,
    bold: true,
    color: C.text,
    align: "center",
    valign: "mid",
    margin: 0,
    fit: "shrink",
    lineSpacingMultiple: opts.lineSpacingMultiple || 1.16,
  });
}

function addConclusionTile(slide, title, body, x, y, w, h, color = C.blue) {
  slide.addShape(pptx.ShapeType.line, {
    x,
    y: y + 0.06,
    w: 0,
    h: h - 0.12,
    line: { color, width: 3.4 },
  });
  slide.addText(title, {
    x: x + 0.18,
    y: y + 0.13,
    w: w - 0.28,
    h: 0.24,
    fontFace: FONT,
    fontSize: 21.8,
    bold: true,
    color,
    margin: 0,
    fit: "shrink",
  });
  slide.addText(body, {
    x: x + 0.18,
    y: y + 0.53,
    w: w - 0.28,
    h: h - 0.62,
    fontFace: FONT,
    fontSize: 18.4,
    color: C.text,
    margin: 0,
    fit: "shrink",
    lineSpacingMultiple: 1.20,
  });
}

function addSpeakerNotes(slide, text) {
  slide.addNotes(text.trim());
}

let slideNo = 0;
function finishSlide(slide, sectionTag, opts = {}) {
  if (sectionTag) addSectionTag(slide, sectionTag);
  addFooter(slide, ++slideNo, opts);
}

function slideCover() {
  const slide = pptx.addSlide();
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: W,
    h: 3.05,
    fill: { color: C.deep },
    line: { color: C.deep },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 3.05,
    w: W,
    h: 0.15,
    fill: { color: "1E9BD7" },
    line: { color: "1E9BD7" },
  });
  if (fs.existsSync(LOGO)) {
    slide.addImage({ path: LOGO, x: 0.45, y: 0.28, w: 1.08, h: 1.25 });
  }
  slide.addText("[Paper Title]\n[Optional Second Line]", {
    x: 1.18,
    y: 0.68,
    w: 11.25,
    h: 1.38,
    fontFace: FONT,
    fontSize: 40.5,
    bold: true,
    color: C.white,
    align: "center",
    margin: 0,
    fit: "shrink",
    lineSpacingMultiple: 1.08,
  });
  slide.addText("[One-line system or method subtitle]", {
    x: 0.82,
    y: 3.63,
    w: 11.70,
    h: 0.34,
    fontFace: FONT,
    fontSize: 24.5,
    bold: true,
    color: C.blue,
    align: "center",
    margin: 0,
  });
  slide.addText("[Presenter Name], [Coauthor A], [Coauthor B]", {
    x: 0.72,
    y: 4.42,
    w: 11.90,
    h: 0.32,
    fontFace: FONT,
    fontSize: 24.0,
    color: C.text,
    align: "center",
    margin: 0,
    fit: "shrink",
  });
  slide.addText("[Institution 1]  |  [Institution 2]", {
    x: 0.82,
    y: 4.94,
    w: 11.70,
    h: 0.25,
    fontFace: FONT,
    fontSize: 18.0,
    color: C.muted,
    align: "center",
    margin: 0,
  });
  finishSlide(slide, "", { logo: false });
  addSpeakerNotes(
    slide,
    `
Introduce the paper, the one-sentence systems question, and the talk plan.
Keep the opening concise, technical, and audience-facing.
    `,
  );
}

function slideResultDominant() {
  const slide = pptx.addSlide();
  addTitle(slide, "[Takeaway result title]");
  addFigure(slide, "result-figure", 0.55, 1.00, 12.25, 3.15);
  metricCard(
    slide,
    "[Metric A]",
    "[what it measures]",
    0.78,
    4.52,
    3.55,
    0.98,
    C.blue,
    C.paleBlue,
    { mainSize: 28, labelSize: 16.4, labelY: 0.50, labelBottom: 0.56, lineSpacingMultiple: 1.06 },
  );
  metricCard(
    slide,
    "[Metric B]",
    "[baseline or trade-off]",
    4.88,
    4.52,
    3.55,
    0.98,
    C.green,
    C.paleGreen,
    { mainSize: 28, labelSize: 16.4, labelY: 0.50, labelBottom: 0.56, lineSpacingMultiple: 1.06 },
  );
  metricCard(
    slide,
    "[Metric C]",
    "[robustness or second view]",
    8.98,
    4.52,
    3.55,
    0.98,
    C.orange,
    C.paleOrange,
    { mainSize: 28, labelSize: 16.4, labelY: 0.50, labelBottom: 0.56, lineSpacingMultiple: 1.06 },
  );
  addTakeaway(slide, "[One sentence the audience should remember.]", 5.98);
  finishSlide(slide, "RESULT");
  addSpeakerNotes(
    slide,
    `
Lead with the evidence figure, then interpret the three numbers in plain English.
Do not list every workload or every axis value aloud.
State what changed, compared with what, and why the result is credible.
    `,
  );
}

function slideConclusion() {
  const slide = pptx.addSlide();
  addTitle(slide, "Conclusion");
  addConclusionTile(slide, "Problem", "[State the unresolved bottleneck.]", 0.68, 1.00, 3.78, 1.50, C.red);
  addConclusionTile(slide, "Insight", "[State the central mechanism or idea.]", 4.78, 1.00, 3.78, 1.50, C.blue);
  addConclusionTile(slide, "Result", "[State the strongest verified outcome.]", 8.88, 1.00, 3.78, 1.50, C.green);
  addConclusionTile(
    slide,
    "Scope",
    "[State where the conclusion applies and where it does not.]",
    0.68,
    2.78,
    5.78,
    1.55,
    C.blue,
  );
  addConclusionTile(
    slide,
    "Next step",
    "[State one follow-up question, limitation, or deployment implication.]",
    6.88,
    2.78,
    5.78,
    1.55,
    C.red,
  );
  slide.addShape(pptx.ShapeType.line, {
    x: 1.05,
    y: 4.76,
    w: 11.20,
    h: 0,
    line: { color: C.line, width: 1.95 },
  });
  slide.addText("[One sentence that resolves the opening question.]", {
    x: 1.00,
    y: 4.98,
    w: 11.35,
    h: 0.48,
    fontFace: FONT,
    fontSize: 25.2,
    bold: true,
    color: C.deep,
    align: "center",
    margin: 0,
    fit: "shrink",
    lineSpacingMultiple: 1.12,
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 6.03,
    w: W,
    h: 0.74,
    fill: { color: C.deep },
    line: { color: C.deep },
  });
  slide.addText("Thanks & Q&A", {
    x: 0.72,
    y: 6.22,
    w: 11.90,
    h: 0.28,
    fontFace: FONT,
    fontSize: 26.0,
    bold: true,
    color: C.white,
    align: "center",
    margin: 0,
  });
  finishSlide(slide, "CLOSE");
  addSpeakerNotes(
    slide,
    `
Restate the contribution as an answer to the opening question.
End on an intellectual conclusion, not only on a polite thank-you.
    `,
  );
}

[slideCover, slideResultDominant, slideConclusion].forEach((build) => build());

pptx.writeFile({ fileName: OUT, compression: true }).then(() => console.log(OUT));

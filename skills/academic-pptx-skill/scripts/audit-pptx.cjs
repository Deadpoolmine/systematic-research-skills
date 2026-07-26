#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const runtimeDir = path.join(__dirname, 'export', 'node_modules');
const JSZip = require(path.join(runtimeDir, 'jszip'));
const { XMLParser } = require(path.join(runtimeDir, 'fast-xml-parser'));

const GRID_W = 160;
const GRID_H = 90;

function parseArgs(argv) {
  const options = {
    input: null,
    json: null,
    minFont: 12,
    minCoverage: 28,
    maxCoverage: 78,
    notesRequired: false,
    strict: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (!value.startsWith('-') && !options.input) options.input = value;
    else if (value === '--json') options.json = argv[++index];
    else if (value === '--min-font') options.minFont = Number(argv[++index]);
    else if (value === '--min-coverage') options.minCoverage = Number(argv[++index]);
    else if (value === '--max-coverage') options.maxCoverage = Number(argv[++index]);
    else if (value === '--notes-required') options.notesRequired = true;
    else if (value === '--strict') options.strict = true;
    else throw new Error(`Unknown argument: ${value}`);
  }
  if (!options.input) {
    throw new Error('Usage: audit-pptx.cjs <deck.pptx> [--json report.json] [--notes-required] [--strict]');
  }
  for (const key of ['minFont', 'minCoverage', 'maxCoverage']) {
    if (!Number.isFinite(options[key]) || options[key] < 0) throw new Error(`Invalid --${key} value.`);
  }
  return options;
}

function asArray(value) {
  if (value === undefined || value === null) return [];
  return Array.isArray(value) ? value : [value];
}

function naturalSlideSort(a, b) {
  const an = Number(a.match(/(?:slide|notesSlide)(\d+)\.xml$/)?.[1] || 0);
  const bn = Number(b.match(/(?:slide|notesSlide)(\d+)\.xml$/)?.[1] || 0);
  return an - bn;
}

function walk(value, visitor, key = null) {
  if (Array.isArray(value)) {
    value.forEach((entry) => walk(entry, visitor, key));
    return;
  }
  if (!value || typeof value !== 'object') return;
  visitor(value, key);
  for (const [childKey, child] of Object.entries(value)) {
    walk(child, visitor, childKey);
  }
}

function collectText(value) {
  const parts = [];
  function visit(node) {
    if (Array.isArray(node)) return node.forEach(visit);
    if (!node || typeof node !== 'object') return;
    for (const [key, child] of Object.entries(node)) {
      if (key === 't') {
        if (typeof child === 'string') parts.push(child);
        else if (child && typeof child['#text'] === 'string') parts.push(child['#text']);
      } else {
        visit(child);
      }
    }
  }
  visit(value);
  return parts.join(' ').replace(/\s+/g, ' ').trim();
}

function shapeBox(shape) {
  const transform = shape?.spPr?.xfrm || shape?.xfrm;
  const off = asArray(transform?.off)[0];
  const ext = asArray(transform?.ext)[0];
  if (!off || !ext) return null;
  const box = {
    x: Number(off.x),
    y: Number(off.y),
    w: Number(ext.cx),
    h: Number(ext.cy),
  };
  return Object.values(box).every(Number.isFinite) ? box : null;
}

function createGrid() {
  return Array.from({ length: GRID_H }, () => new Uint8Array(GRID_W));
}

function markGrid(grid, box, slideWidth, slideHeight) {
  if (!box || box.w <= 0 || box.h <= 0) return;
  const x0 = Math.max(0, Math.min(GRID_W, Math.floor((box.x / slideWidth) * GRID_W)));
  const y0 = Math.max(0, Math.min(GRID_H, Math.floor((box.y / slideHeight) * GRID_H)));
  const x1 = Math.max(0, Math.min(GRID_W, Math.ceil(((box.x + box.w) / slideWidth) * GRID_W)));
  const y1 = Math.max(0, Math.min(GRID_H, Math.ceil(((box.y + box.h) / slideHeight) * GRID_H)));
  for (let y = y0; y < y1; y += 1) {
    for (let x = x0; x < x1; x += 1) grid[y][x] = 1;
  }
}

function gridCoverage(grid) {
  let marked = 0;
  grid.forEach((row) => row.forEach((value) => { marked += value; }));
  return Number(((marked / (GRID_W * GRID_H)) * 100).toFixed(1));
}

function increment(map, value) {
  if (value === undefined || value === null || value === '') return;
  const key = String(value);
  map.set(key, (map.get(key) || 0) + 1);
}

function topEntries(map, limit = 12, numeric = false) {
  return [...map.entries()]
    .map(([value, count]) => ({ value: numeric ? Number(value) : value, count }))
    .sort((a, b) => b.count - a.count || String(a.value).localeCompare(String(b.value)))
    .slice(0, limit);
}

function collectFormatting(shape, stats, minFont) {
  walk(shape, (node, key) => {
    if (['rPr', 'defRPr', 'endParaRPr'].includes(key) && node.sz !== undefined) {
      const points = Number(node.sz) / 100;
      if (Number.isFinite(points)) {
        increment(stats.fontSizes, points.toFixed(1));
        if (points < minFont) stats.lowFonts.push(Number(points.toFixed(1)));
      }
    }
    if (['latin', 'ea', 'cs'].includes(key) && node.typeface) increment(stats.fonts, node.typeface);
    if (key === 'srgbClr' && node.val) increment(stats.colors, node.val.toUpperCase());
    if (key === 'schemeClr' && node.val) increment(stats.colors, node.val);
  });
}

function collectShapes(tree) {
  const result = { text: [], pictures: [], graphics: [] };
  function visit(group) {
    asArray(group?.sp).forEach((shape) => result.text.push(shape));
    asArray(group?.pic).forEach((shape) => result.pictures.push(shape));
    asArray(group?.graphicFrame).forEach((shape) => result.graphics.push(shape));
    asArray(group?.grpSp).forEach(visit);
  }
  visit(tree);
  return result;
}

function outside(box, width, height) {
  const tolerance = 1000;
  return box && (
    box.x < -tolerance || box.y < -tolerance ||
    box.x + box.w > width + tolerance || box.y + box.h > height + tolerance
  );
}

async function parseXml(zip, parser, name) {
  const file = zip.file(name);
  if (!file) return null;
  return parser.parse(await file.async('string'));
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const inputPath = path.resolve(options.input);
  if (!fs.existsSync(inputPath)) throw new Error(`PPTX not found: ${inputPath}`);

  const parser = new XMLParser({
    ignoreAttributes: false,
    attributeNamePrefix: '',
    removeNSPrefix: true,
    trimValues: false,
  });
  const zip = await JSZip.loadAsync(fs.readFileSync(inputPath));
  const presentation = await parseXml(zip, parser, 'ppt/presentation.xml');
  const size = presentation?.presentation?.sldSz;
  const slideWidth = Number(size?.cx || 12192000);
  const slideHeight = Number(size?.cy || 6858000);
  const slideFiles = Object.keys(zip.files).filter((name) => /^ppt\/slides\/slide\d+\.xml$/.test(name)).sort(naturalSlideSort);
  const noteFiles = Object.keys(zip.files).filter((name) => /^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(name)).sort(naturalSlideSort);
  const globalStats = { fontSizes: new Map(), fonts: new Map(), colors: new Map() };
  const slides = [];
  const errors = [];
  const warnings = [];

  for (let index = 0; index < slideFiles.length; index += 1) {
    const parsed = await parseXml(zip, parser, slideFiles[index]);
    const tree = parsed?.sld?.cSld?.spTree;
    const shapes = collectShapes(tree);
    const textGrid = createGrid();
    const visualGrid = createGrid();
    const objectGrid = createGrid();
    const slideStats = { fontSizes: globalStats.fontSizes, fonts: globalStats.fonts, colors: globalStats.colors, lowFonts: [] };
    let outOfBounds = 0;
    let textBoxes = 0;

    shapes.text.forEach((shape) => {
      const text = collectText(shape);
      const box = shapeBox(shape);
      collectFormatting(shape, slideStats, options.minFont);
      if (!text || !box) return;
      textBoxes += 1;
      markGrid(textGrid, box, slideWidth, slideHeight);
      markGrid(objectGrid, box, slideWidth, slideHeight);
      if (outside(box, slideWidth, slideHeight)) outOfBounds += 1;
    });
    [...shapes.pictures, ...shapes.graphics].forEach((shape) => {
      const box = shapeBox(shape);
      collectFormatting(shape, slideStats, options.minFont);
      if (!box) return;
      markGrid(visualGrid, box, slideWidth, slideHeight);
      markGrid(objectGrid, box, slideWidth, slideHeight);
      if (outside(box, slideWidth, slideHeight)) outOfBounds += 1;
    });

    const item = {
      slide: index + 1,
      textBoxes,
      pictures: shapes.pictures.length,
      graphics: shapes.graphics.length,
      textCoverage: gridCoverage(textGrid),
      visualCoverage: gridCoverage(visualGrid),
      objectCoverage: gridCoverage(objectGrid),
      fontsBelowThreshold: slideStats.lowFonts,
      outOfBounds,
    };
    slides.push(item);
    if (outOfBounds) errors.push(`slide ${item.slide}: ${outOfBounds} object(s) outside the canvas`);
    if (slideStats.lowFonts.length) {
      warnings.push(`slide ${item.slide}: ${slideStats.lowFonts.length} explicit font run(s) below ${options.minFont} pt`);
    }
    const isEdgePage = index === 0 || index === slideFiles.length - 1;
    if (!isEdgePage && item.objectCoverage < options.minCoverage) {
      warnings.push(`slide ${item.slide}: sparse object coverage ${item.objectCoverage}%`);
    }
    if (!isEdgePage && item.objectCoverage > options.maxCoverage) {
      warnings.push(`slide ${item.slide}: dense object coverage ${item.objectCoverage}%`);
    }
  }

  let notesWithContent = 0;
  for (const file of noteFiles) {
    const parsed = await parseXml(zip, parser, file);
    const text = collectText(parsed).replace(/\b\d{1,3}\b/g, '').trim();
    if (text.length >= 20) notesWithContent += 1;
  }
  if (options.notesRequired && notesWithContent !== slideFiles.length) {
    errors.push(`speaker notes present on ${notesWithContent}/${slideFiles.length} slides`);
  }

  const average = (field) => Number((slides.reduce((sum, slide) => sum + slide[field], 0) / Math.max(1, slides.length)).toFixed(1));
  const report = {
    file: inputPath,
    generatedAt: new Date().toISOString(),
    thresholds: {
      minFontPt: options.minFont,
      reviewCoveragePercent: [options.minCoverage, options.maxCoverage],
      notesRequired: options.notesRequired,
    },
    summary: {
      slides: slideFiles.length,
      notesFiles: noteFiles.length,
      notesWithContent,
      sizeInches: [Number((slideWidth / 914400).toFixed(3)), Number((slideHeight / 914400).toFixed(3))],
      averageTextCoverage: average('textCoverage'),
      averageVisualCoverage: average('visualCoverage'),
      averageObjectCoverage: average('objectCoverage'),
      explicitFonts: topEntries(globalStats.fonts),
      explicitFontSizesPt: topEntries(globalStats.fontSizes, 16, true),
      colors: topEntries(globalStats.colors),
      errors: errors.length,
      warnings: warnings.length,
    },
    slides,
    errors,
    warnings,
  };

  if (options.json) {
    const outputPath = path.resolve(options.json);
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  }

  console.log(`[pptx-audit] slides=${report.summary.slides} notes=${notesWithContent}/${slideFiles.length}`);
  console.log(`[pptx-audit] avg text=${report.summary.averageTextCoverage}% visual=${report.summary.averageVisualCoverage}% objects=${report.summary.averageObjectCoverage}%`);
  console.log(`[pptx-audit] errors=${errors.length} warnings=${warnings.length}`);
  warnings.slice(0, 12).forEach((warning) => console.log(`[warning] ${warning}`));
  errors.forEach((error) => console.error(`[error] ${error}`));
  if (options.json) console.log(`[pptx-audit] report=${path.resolve(options.json)}`);
  if (options.strict && errors.length) process.exitCode = 2;
}

main().catch((error) => {
  console.error(`[pptx-audit] ${error.message}`);
  process.exit(1);
});

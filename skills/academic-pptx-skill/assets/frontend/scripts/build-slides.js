#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import postcss from 'postcss';
import tailwindcss from 'tailwindcss';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(scriptDir, '..');
const slidesDir = path.join(rootDir, 'src', 'slides');
const outputDir = path.join(rootDir, 'dist-slides');

function extractSlide(source, fileName) {
  const match = source.match(/window\.slideDataMap\.set\(\s*(\d+)\s*,\s*`([\s\S]*?)`\s*\);/);
  if (!match) throw new Error(`Cannot parse ${fileName}; expected window.slideDataMap.set(N, \`...\`).`);
  return { number: Number(match[1]), content: match[2].trim() };
}

function collectSlides() {
  return fs.readdirSync(slidesDir)
    .filter((name) => /^slide-\d+\.js$/.test(name))
    .map((name) => extractSlide(fs.readFileSync(path.join(slidesDir, name), 'utf8'), name))
    .sort((a, b) => a.number - b.number);
}

async function buildTailwind(slides) {
  const sourcePath = path.join(rootDir, 'src', 'styles', 'main.css');
  const sourceCss = fs.readFileSync(sourcePath, 'utf8');
  const result = await postcss([
    tailwindcss({
      content: [{ raw: slides.map((slide) => slide.content).join('\n'), extension: 'html' }],
      theme: { extend: {} },
      plugins: []
    })
  ]).process(sourceCss, { from: sourcePath });
  return result.css;
}

function normalizeAssetPaths(html) {
  return html.replace(/src=(['"])\/assets\//g, 'src=$1assets/');
}

function copyDirectory(source, destination) {
  fs.mkdirSync(destination, { recursive: true });
  for (const entry of fs.readdirSync(source, { withFileTypes: true })) {
    const from = path.join(source, entry.name);
    const to = path.join(destination, entry.name);
    if (entry.isDirectory()) copyDirectory(from, to);
    else fs.copyFileSync(from, to);
  }
}

function prepareSlide(content) {
  let result = normalizeAssetPaths(content);
  result = result.replace(/<div([^>]*)>/i, (tag, attrs) => {
    if (/class=['"][^'"]*slide-page/.test(attrs)) return tag;
    if (/class=['"]/.test(attrs)) return `<div${attrs.replace(/class=(['"])/, 'class=$1slide-page ')}>`;
    return `<div class="slide-page"${attrs}>`;
  });
  return result;
}

async function main() {
  console.log('[build:slides] Collecting slide files');
  const slides = collectSlides();
  if (slides.length === 0) throw new Error(`No slide-N.js files found in ${slidesDir}`);
  fs.rmSync(outputDir, { recursive: true, force: true });
  fs.mkdirSync(outputDir, { recursive: true });
  console.log('[build:slides] Compiling Tailwind CSS');
  const css = await buildTailwind(slides);
  console.log('[build:slides] Preparing merged HTML');
  const bodies = slides.map((slide) => prepareSlide(slide.content));
  const indexHtml = fs.readFileSync(path.join(rootDir, 'index.html'), 'utf8');
  const rootStyle = indexHtml.match(/<style[^>]*>([\s\S]*?)<\/style>/i)?.[1] || '';
  const html = `<!doctype html><html><head><meta charset="UTF-8"><style>${rootStyle}\n${css}\nhtml,body{margin:0;padding:0;} .slide-page{width:1440px;height:810px;overflow:hidden;}</style></head><body>${bodies.join('\n')}</body></html>`;
  fs.writeFileSync(path.join(outputDir, 'all-slides.html'), html, 'utf8');
  const assets = path.join(rootDir, 'public', 'assets');
  if (fs.existsSync(assets)) copyDirectory(assets, path.join(outputDir, 'assets'));
  console.log(`[build:slides] Built ${slides.length} slides in ${outputDir}`);
}

main().catch((error) => {
  console.error(`[build:slides] ${error.message}`);
  process.exit(1);
});

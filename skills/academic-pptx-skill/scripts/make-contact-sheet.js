#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const sharp = require(path.join(__dirname, 'export', 'node_modules', 'sharp'));

const inputDir = path.resolve(process.argv[2] || '.');
const outputPath = path.resolve(process.argv[3] || 'contact-sheet.png');
const files = fs.readdirSync(inputDir)
  .filter((file) => /\.(png|jpe?g)$/i.test(file))
  .sort((a, b) => Number(a.match(/(\d+)/)?.[1] || 0) - Number(b.match(/(\d+)/)?.[1] || 0) || a.localeCompare(b));

if (!files.length) {
  console.error(`[contact-sheet] No slide images found in ${inputDir}`);
  process.exit(1);
}

const thumbWidth = 560;
const thumbHeight = 315;
const labelHeight = 34;
const columns = 3;
const gap = 22;
const rows = Math.ceil(files.length / columns);
const canvasWidth = columns * thumbWidth + (columns + 1) * gap;
const canvasHeight = rows * (thumbHeight + labelHeight) + (rows + 1) * gap;

async function main() {
  const composites = [];
  for (let index = 0; index < files.length; index += 1) {
    const row = Math.floor(index / columns);
    const column = index % columns;
    const left = gap + column * (thumbWidth + gap);
    const top = gap + row * (thumbHeight + labelHeight + gap);
    const image = await sharp(path.join(inputDir, files[index]))
      .resize(thumbWidth, thumbHeight, { fit: 'contain', background: '#ffffff' })
      .png()
      .toBuffer();
    const label = Buffer.from(`<svg width="${thumbWidth}" height="${labelHeight}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#f3f5f7"/><text x="8" y="24" font-family="Arial" font-size="18" fill="#333333">Slide ${index + 1}</text></svg>`);
    composites.push({ input: image, left, top });
    composites.push({ input: label, left, top: top + thumbHeight });
  }
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  await sharp({
    create: { width: canvasWidth, height: canvasHeight, channels: 4, background: '#e8edf2' },
  }).composite(composites).png().toFile(outputPath);
  console.log(`[contact-sheet] ${outputPath}`);
}

main().catch((error) => {
  console.error(`[contact-sheet] ${error.message}`);
  process.exit(1);
});

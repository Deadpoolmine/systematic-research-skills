#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function run(command, args, cwd) {
  const result = spawnSync(command, args, {
    cwd,
    stdio: 'inherit',
    shell: process.platform === 'win32' && /\.(cmd|bat)$/i.test(command)
  });
  if (result.status !== 0) {
    throw new Error(`Command failed (${result.status}): ${command} ${args.join(' ')}`);
  }
}

function main() {
  const [skillDirArg, workspaceDirArg, ...flags] = process.argv.slice(2);
  if (!skillDirArg || !workspaceDirArg) {
    console.error('Usage: node export-ppt.js <SKILL_DIR> <WORKSPACE_DIR> [--debug]');
    process.exit(1);
  }

  const skillDir = path.resolve(skillDirArg);
  const workspaceDir = path.resolve(workspaceDirArg);
  const frontendDir = path.join(workspaceDir, 'frontend');
  const slidesDir = path.join(frontendDir, 'src', 'slides');
  const converter = path.join(skillDir, 'scripts', 'export', 'html2pptx.js');
  const mergedHtml = path.join(frontendDir, 'dist-slides', 'all-slides.html');
  const outputDir = path.join(workspaceDir, 'artifacts');
  const outputPptx = path.join(outputDir, 'presentation.pptx');

  if (!fs.existsSync(frontendDir)) throw new Error(`Frontend not found: ${frontendDir}`);
  if (!fs.existsSync(converter)) throw new Error(`PptxGenJS converter not found: ${converter}`);
  const slides = fs.existsSync(slidesDir)
    ? fs.readdirSync(slidesDir).filter((name) => /^slide-\d+\.js$/.test(name))
    : [];
  if (slides.length === 0) throw new Error(`No slide-N.js files found in ${slidesDir}`);

  run(process.execPath, [path.join(frontendDir, 'scripts', 'build-slides.js')], frontendDir);
  fs.mkdirSync(outputDir, { recursive: true });

  const converterArgs = [converter, mergedHtml, outputPptx];
  if (flags.includes('--debug')) converterArgs.push('--debug');
  run(process.execPath, converterArgs, workspaceDir);

  if (!fs.existsSync(outputPptx) || fs.statSync(outputPptx).size === 0) {
    throw new Error(`PPTX was not created: ${outputPptx}`);
  }
  console.log(`[export] Created ${outputPptx}`);
}

try {
  main();
} catch (error) {
  console.error(`[export] ${error.message}`);
  process.exit(1);
}

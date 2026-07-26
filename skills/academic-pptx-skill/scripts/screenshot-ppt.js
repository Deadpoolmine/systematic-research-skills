#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { chromium } = require(path.join(__dirname, 'export', 'node_modules', 'playwright'));

function readArgs(argv) {
  const options = { url: 'http://localhost:5173', output: null, pages: null, auditOutput: null, strict: false };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--url') options.url = argv[++index];
    else if (value === '--output' || value === '-o') options.output = argv[++index];
    else if (value === '--pages' || value === '-p') options.pages = Number(argv[++index]);
    else if (value === '--audit-output') options.auditOutput = argv[++index];
    else if (value === '--strict') options.strict = true;
    else throw new Error(`Unknown argument: ${value}`);
  }
  if (!options.output) throw new Error('--output is required.');
  if (options.pages !== null && (!Number.isInteger(options.pages) || options.pages < 1)) {
    throw new Error('--pages must be a positive integer.');
  }
  return options;
}

async function launchBrowser() {
  const launchOptions = {};
  if (process.env.PPTX_BROWSER_EXECUTABLE) {
    launchOptions.executablePath = process.env.PPTX_BROWSER_EXECUTABLE;
  } else if (process.env.PPTX_BROWSER_CHANNEL) {
    launchOptions.channel = process.env.PPTX_BROWSER_CHANNEL;
  } else if (process.platform === 'win32' || process.platform === 'darwin') {
    launchOptions.channel = 'chrome';
  }
  try {
    return await chromium.launch(launchOptions);
  } catch (error) {
    if (!launchOptions.channel) throw error;
    delete launchOptions.channel;
    return chromium.launch(launchOptions);
  }
}

async function main() {
  const options = readArgs(process.argv.slice(2));
  const outputDir = path.resolve(options.output);
  const auditPath = path.resolve(options.auditOutput || path.join(outputDir, 'browser-audit.json'));
  fs.mkdirSync(outputDir, { recursive: true });
  const browser = await launchBrowser();
  try {
    const context = await browser.newContext({ viewport: { width: 1480, height: 850 } });
    const page = await context.newPage();
    const baseUrl = options.url.replace(/\/$/, '');
    await page.goto(`${baseUrl}?page=1`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.addStyleTag({ content: '.nav-btn,.progress-bar,.page-indicator{display:none!important}' });
    const total = options.pages || await page.evaluate(() => window.slideDataMap?.size || 0);
    if (total < 1) throw new Error('No slides detected; verify the preview server and slide-N.js files.');
    const audit = { generatedAt: new Date().toISOString(), url: baseUrl, slides: [], errors: [], warnings: [] };
    for (let number = 1; number <= total; number += 1) {
      await page.goto(`${baseUrl}?page=${number}`, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await page.addStyleTag({ content: '.nav-btn,.progress-bar,.page-indicator{display:none!important}' });
      const result = await page.evaluate((slideNumber) => {
        const active = document.querySelector('.slide.active');
        const root = active?.firstElementChild || active;
        const errors = [];
        const warnings = [];
        if (!root) return { slide: slideNumber, errors: ['active slide root not found'], warnings };
        if (root.clientWidth !== 1440 || root.clientHeight !== 810) {
          errors.push(`root is ${root.clientWidth}x${root.clientHeight}; expected 1440x810`);
        }
        const rootBox = root.getBoundingClientRect();
        const textSelectors = 'h1,h2,h3,h4,p,li,td,th,figcaption,span';
        const fontSizes = [];
        root.querySelectorAll(textSelectors).forEach((element) => {
          const text = (element.textContent || '').replace(/\s+/g, ' ').trim();
          if (!text) return;
          const box = element.getBoundingClientRect();
          const style = getComputedStyle(element);
          const size = Number.parseFloat(style.fontSize);
          if (Number.isFinite(size)) fontSizes.push(size);
          const outside = box.left < rootBox.left - 1 || box.top < rootBox.top - 1 || box.right > rootBox.right + 1 || box.bottom > rootBox.bottom + 1;
          if (outside) errors.push(`${element.tagName.toLowerCase()} text outside slide: ${text.slice(0, 60)}`);
          const clipped = element.clientWidth > 0 && element.clientHeight > 0 &&
            (element.scrollWidth > element.clientWidth + 2 || element.scrollHeight > element.clientHeight + 2);
          if (clipped && style.overflow !== 'visible') errors.push(`${element.tagName.toLowerCase()} text clipped: ${text.slice(0, 60)}`);
        });
        root.querySelectorAll('img').forEach((image) => {
          if (!image.complete || image.naturalWidth < 1 || image.naturalHeight < 1) {
            errors.push(`broken image: ${image.getAttribute('src') || '[missing src]'}`);
          }
        });
        if (root.scrollWidth > root.clientWidth + 2 || root.scrollHeight > root.clientHeight + 2) {
          warnings.push(`root scroll area ${root.scrollWidth}x${root.scrollHeight} exceeds 1440x810`);
        }
        return {
          slide: slideNumber,
          root: [root.clientWidth, root.clientHeight],
          minimumTextPx: fontSizes.length ? Math.min(...fontSizes) : null,
          errors,
          warnings,
        };
      }, number);
      result.errors.forEach((error) => audit.errors.push(`slide ${number}: ${error}`));
      result.warnings.forEach((warning) => audit.warnings.push(`slide ${number}: ${warning}`));
      audit.slides.push(result);
      await page.locator('#ppt-viewport').screenshot({ path: path.join(outputDir, `page-${number}.png`) });
    }
    fs.mkdirSync(path.dirname(auditPath), { recursive: true });
    fs.writeFileSync(auditPath, `${JSON.stringify(audit, null, 2)}\n`, 'utf8');
    console.log(`[screenshot] Captured ${total} slides in ${outputDir}`);
    console.log(`[screenshot] Audit errors=${audit.errors.length} warnings=${audit.warnings.length} report=${auditPath}`);
    if (options.strict && audit.errors.length) process.exitCode = 2;
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(`[screenshot] ${error.message}`);
  process.exit(1);
});

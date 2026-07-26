#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const options = {
    input: null,
    json: null,
    slides: null,
    language: 'any',
    minMinutes: null,
    maxMinutes: null,
    strict: false,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if ((value === '-' || !value.startsWith('-')) && !options.input) options.input = value;
    else if (value === '--json') options.json = argv[++index];
    else if (value === '--slides') options.slides = Number(argv[++index]);
    else if (value === '--language') options.language = String(argv[++index] || 'any').toLowerCase();
    else if (value === '--min-minutes') options.minMinutes = Number(argv[++index]);
    else if (value === '--max-minutes') options.maxMinutes = Number(argv[++index]);
    else if (value === '--strict') options.strict = true;
    else throw new Error(`Unknown argument: ${value}`);
  }
  if (!options.input) {
    throw new Error(
      'Usage: verify-speaker-notes.cjs <speaker-notes.txt|-> [--slides N] [--language any|en] [--min-minutes M] [--max-minutes M] [--json report.json] [--strict]',
    );
  }
  if (options.slides !== null && (!Number.isFinite(options.slides) || options.slides <= 0)) {
    throw new Error('Invalid --slides value.');
  }
  for (const key of ['minMinutes', 'maxMinutes']) {
    if (options[key] !== null && (!Number.isFinite(options[key]) || options[key] <= 0)) {
      throw new Error(`Invalid --${key} value.`);
    }
  }
  if (!['any', 'en'].includes(options.language)) {
    throw new Error('Invalid --language value. Use `any` or `en`.');
  }
  return options;
}

function countWords(text) {
  return (text.match(/[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?/g) || []).length;
}

function countCjk(text) {
  return (text.match(/[\u3400-\u9fff]/g) || []).length;
}

function countMatches(text, pattern) {
  return (text.match(pattern) || []).length;
}

function extractSections(content) {
  const normalized = content.replace(/\r\n/g, '\n');
  const regex = /^Slide\s+\[(\d+)\]\s*-\s*(.+)$/gm;
  const matches = [...normalized.matchAll(regex)];
  const sections = [];
  for (let index = 0; index < matches.length; index += 1) {
    const current = matches[index];
    const next = matches[index + 1];
    const start = current.index;
    const end = next ? next.index : normalized.length;
    sections.push({
      slide: Number(current[1]),
      title: current[2].trim(),
      raw: normalized.slice(start, end).trim(),
    });
  }
  return sections;
}

function parseDeclaredSeconds(sectionText) {
  const match = sectionText.match(
    /(^|\n)Time:\s*([0-9]+(?:\.[0-9]+)?)\s*(seconds?|secs?|s|minutes?|mins?|min)?/i,
  );
  if (!match) return null;
  const value = Number(match[2]);
  if (!Number.isFinite(value)) return null;
  const unit = (match[3] || 'seconds').toLowerCase();
  if (unit.startsWith('min')) return value * 60;
  return value;
}

function analyzeSection(section) {
  const raw = section.raw;
  return {
    slide: section.slide,
    title: section.title,
    words: countWords(raw),
    hasPurpose: /(^|\n)Purpose:\s+\S+/m.test(raw),
    hasTime: /(^|\n)Time:\s+\S+/m.test(raw),
    hasTalkTrack: /(^|\n)Talk track:\s*/m.test(raw),
    hasTransition: /(^|\n)Transition:\s*/m.test(raw),
    hasPresenterCues: /(^|\n)Presenter cues:\s*/m.test(raw),
    likelyQuestions: countMatches(raw, /(^|\n)Likely question:\s*/gm),
    sourcesBlocks: countMatches(raw, /\[Sources\]/g),
    declaredSeconds: parseDeclaredSeconds(raw),
    cjkChars: countCjk(raw),
  };
}

function expectedSequence(maxSlide) {
  const result = [];
  for (let value = 1; value <= maxSlide; value += 1) result.push(value);
  return result;
}

function durationSummary(words) {
  return {
    duration120wpm: Number((words / 120).toFixed(1)),
    duration130wpm: Number((words / 130).toFixed(1)),
    duration140wpm: Number((words / 140).toFixed(1)),
  };
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const fromStdin = options.input === '-';
  const inputPath = fromStdin ? '<stdin>' : path.resolve(options.input);
  if (!fromStdin && !fs.existsSync(inputPath)) throw new Error(`Notes file not found: ${inputPath}`);

  const content = fromStdin ? fs.readFileSync(0, 'utf8') : fs.readFileSync(inputPath, 'utf8');
  const sections = extractSections(content);
  const warnings = [];
  const errors = [];

  if (!sections.length) {
    throw new Error('No `Slide [N] - Title` sections were found.');
  }

  const analyses = sections.map(analyzeSection);
  const slideNumbers = analyses.map((item) => item.slide);
  const duplicates = slideNumbers.filter((slide, index) => slideNumbers.indexOf(slide) !== index);
  if (duplicates.length) {
    errors.push(`duplicate slide numbers: ${[...new Set(duplicates)].join(', ')}`);
  }

  const maxExpectedSlide = options.slides ?? Math.max(...slideNumbers);
  const expected = expectedSequence(maxExpectedSlide);
  const missing = expected.filter((slide) => !slideNumbers.includes(slide));
  if (missing.length) {
    const message = `missing slide numbers in notes sequence: ${missing.join(', ')}`;
    if (options.slides !== null) errors.push(message);
    else warnings.push(message);
  }
  const outOfRange = slideNumbers.filter((slide) => slide > maxExpectedSlide);
  if (outOfRange.length) errors.push(`slide numbers exceed expected range: ${[...new Set(outOfRange)].join(', ')}`);

  if (options.slides !== null && analyses.length !== options.slides) {
    errors.push(`parsed ${analyses.length} note section(s), expected ${options.slides}`);
  }

  analyses.forEach((item) => {
    if (!item.hasPurpose) warnings.push(`slide ${item.slide}: missing Purpose field`);
    if (!item.hasTime) warnings.push(`slide ${item.slide}: missing Time field`);
    if (!item.hasTalkTrack) warnings.push(`slide ${item.slide}: missing Talk track section`);
    if (!item.hasTransition) warnings.push(`slide ${item.slide}: missing Transition section`);
  });

  const totalWords = analyses.reduce((sum, item) => sum + item.words, 0);
  const totalCjk = analyses.reduce((sum, item) => sum + item.cjkChars, 0);
  const durations = durationSummary(totalWords);
  const declaredSeconds = analyses.reduce((sum, item) => sum + (item.declaredSeconds || 0), 0);
  const declaredMinutes = Number((declaredSeconds / 60).toFixed(1));

  if (options.language === 'en' && totalCjk > 0) {
    warnings.push(`English notes contain ${totalCjk} CJK character(s)`);
  }
  if (options.minMinutes !== null && durations.duration130wpm < options.minMinutes) {
    warnings.push(`estimated 130 wpm duration ${durations.duration130wpm} min is below ${options.minMinutes} min`);
  }
  if (options.maxMinutes !== null && durations.duration120wpm > options.maxMinutes) {
    warnings.push(`estimated 120 wpm duration ${durations.duration120wpm} min exceeds ${options.maxMinutes} min`);
  }

  const report = {
    file: inputPath,
    generatedAt: new Date().toISOString(),
    assumptions: {
      language: options.language,
      expectedSlides: options.slides,
      minMinutes: options.minMinutes,
      maxMinutes: options.maxMinutes,
    },
    summary: {
      slidesParsed: analyses.length,
      totalWords,
      totalCjkChars: totalCjk,
      duration120wpm: durations.duration120wpm,
      duration130wpm: durations.duration130wpm,
      duration140wpm: durations.duration140wpm,
      declaredMinutes: Number.isFinite(declaredMinutes) ? declaredMinutes : 0,
      slidesWithPurpose: analyses.filter((item) => item.hasPurpose).length,
      slidesWithTime: analyses.filter((item) => item.hasTime).length,
      slidesWithTalkTrack: analyses.filter((item) => item.hasTalkTrack).length,
      slidesWithTransition: analyses.filter((item) => item.hasTransition).length,
      slidesWithSources: analyses.filter((item) => item.sourcesBlocks > 0).length,
      totalLikelyQuestions: analyses.reduce((sum, item) => sum + item.likelyQuestions, 0),
      warnings: warnings.length,
      errors: errors.length,
    },
    slides: analyses.map((item) => ({
      slide: item.slide,
      title: item.title,
      words: item.words,
      declaredSeconds: item.declaredSeconds,
      hasPurpose: item.hasPurpose,
      hasTime: item.hasTime,
      hasTalkTrack: item.hasTalkTrack,
      hasTransition: item.hasTransition,
      hasPresenterCues: item.hasPresenterCues,
      likelyQuestions: item.likelyQuestions,
      sourcesBlocks: item.sourcesBlocks,
      cjkChars: item.cjkChars,
    })),
    warnings,
    errors,
  };

  if (options.json) {
    const outputPath = path.resolve(options.json);
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    fs.writeFileSync(outputPath, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
  }

  console.log(`[notes-verify] slides=${report.summary.slidesParsed} words=${report.summary.totalWords}`);
  console.log(
    `[notes-verify] duration120=${report.summary.duration120wpm}m duration130=${report.summary.duration130wpm}m duration140=${report.summary.duration140wpm}m`,
  );
  if (declaredSeconds > 0) console.log(`[notes-verify] declared=${declaredMinutes}m`);
  console.log(
    `[notes-verify] fields purpose=${report.summary.slidesWithPurpose}/${report.summary.slidesParsed} talk=${report.summary.slidesWithTalkTrack}/${report.summary.slidesParsed} transition=${report.summary.slidesWithTransition}/${report.summary.slidesParsed}`,
  );
  warnings.slice(0, 20).forEach((warning) => console.log(`[warning] ${warning}`));
  errors.forEach((error) => console.error(`[error] ${error}`));
  if (options.json) console.log(`[notes-verify] report=${path.resolve(options.json)}`);

  if (options.strict && errors.length) process.exitCode = 2;
}

try {
  main();
} catch (error) {
  console.error(`[notes-verify] ${error.message}`);
  process.exit(1);
}

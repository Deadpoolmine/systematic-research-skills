#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function copyDirectory(source, destination) {
  fs.mkdirSync(destination, { recursive: true });
  for (const entry of fs.readdirSync(source, { withFileTypes: true })) {
    if (['node_modules', 'dist', 'dist-slides'].includes(entry.name)) continue;
    const from = path.join(source, entry.name);
    const to = path.join(destination, entry.name);
    if (entry.isDirectory()) copyDirectory(from, to);
    else fs.copyFileSync(from, to);
  }
}

function resolvePackageManager() {
  const candidates = process.platform === 'win32'
    ? [['pnpm.cmd', 'pnpm'], ['npm.cmd', 'npm']]
    : [['pnpm', 'pnpm'], ['npm', 'npm']];
  for (const [command, name] of candidates) {
    const probe = spawnSync(command, ['--version'], { shell: process.platform === 'win32' });
    if (probe.status === 0) return { command, name };
  }
  throw new Error('Neither npm nor pnpm is available on PATH.');
}

function installDependencies(directory, packageManager) {
  const result = spawnSync(packageManager.command, ['install'], {
    cwd: directory,
    stdio: 'inherit',
    shell: process.platform === 'win32'
  });
  if (result.status !== 0) {
    throw new Error(`${packageManager.name} install failed in ${directory}`);
  }
}

function main() {
  const [skillDirArg, workspaceDirArg, ...flags] = process.argv.slice(2);
  if (!skillDirArg || !workspaceDirArg) {
    console.error('Usage: node setup.js <SKILL_DIR> <WORKSPACE_DIR> [--skip-install]');
    process.exit(1);
  }

  const skillDir = path.resolve(skillDirArg);
  const workspaceDir = path.resolve(workspaceDirArg);
  const frontendTemplate = path.join(skillDir, 'assets', 'frontend');
  const frontendDir = path.join(workspaceDir, 'frontend');
  const exportDir = path.join(skillDir, 'scripts', 'export');

  if (!fs.existsSync(frontendTemplate)) {
    throw new Error(`Frontend template not found: ${frontendTemplate}`);
  }

  if (!fs.existsSync(frontendDir)) {
    copyDirectory(frontendTemplate, frontendDir);
    console.log(`[setup] Created ${frontendDir}`);
  } else {
    console.log(`[setup] Reusing existing ${frontendDir}`);
  }

  const docsDir = path.join(workspaceDir, 'docs');
  const workDir = path.join(docsDir, 'work');
  const artifactsDir = path.join(workspaceDir, 'artifacts');
  fs.mkdirSync(workDir, { recursive: true });
  fs.mkdirSync(artifactsDir, { recursive: true });
  fs.writeFileSync(
    path.join(docsDir, 'project.json'),
    JSON.stringify({ project_type: 'academic-ppt', renderer: 'pptxgenjs' }, null, 2),
    'utf8'
  );

  if (!flags.includes('--skip-install')) {
    const packageManager = resolvePackageManager();
    console.log(`[setup] Installing dependencies with ${packageManager.name}`);
    installDependencies(frontendDir, packageManager);
    installDependencies(exportDir, packageManager);
  }

  console.log(`[setup] Academic PPTX workspace ready: ${workspaceDir}`);
}

try {
  main();
} catch (error) {
  console.error(`[setup] ${error.message}`);
  process.exit(1);
}

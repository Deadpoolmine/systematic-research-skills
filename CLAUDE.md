# Systematic Research Skills

Research methodology skills for coding agents — structured paper writing, persona-driven peer review, and knowledge synthesis.

## Project Conventions

### Skill Development

Skills follow the [writing-skills](.github/skills/writing-skills/SKILL.md) methodology.

**Style reference:** Skills use [superpowers](https://github.com/prime-radiant-inc/superpowers)-level conciseness — sharp `<HARD-GATE>` tags, flowcharts as primary structure, no verbose tables or rationalization sections. 

### Directory Structure

```
skills/<name>/
  SKILL.md           # Main reference (required) — concise, flowchart-driven
  *.md               # Supporting references (heavy content only)
  scripts/           # Reusable tools (cross-platform: .cmd + .sh)
  templates/         # Discoverable templates — agent lists, not hardcodes
```

### Key Rules

- **Never hardcode template paths.** Agents list `templates/` recursively to discover available types.
- **Scripts must support Windows + Linux.** Every script has `.cmd` and `.sh` variants.
- **`SKILL.md` is the entry point.** Supporting files are loaded on demand, not force-loaded with `@` syntax.
- **Description field is trigger-only.** Start with "Use when..." — never summarize the skill's workflow.

### Agent Behavior

When working in this repo:
- Write `SKILL.md` first, then supporting files as needed
- When a skill references templates, tell the agent to list `templates/` — never assume what's there
- Cross-platform: provide both `.cmd` (Windows) and `.sh` (Linux/macOS) scripts
- Keep `SKILL.md` under 100 lines — move details to supporting files

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

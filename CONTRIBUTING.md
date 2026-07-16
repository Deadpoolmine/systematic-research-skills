# Contributing to Systematic Research Skills

## If You Are an AI Agent

Before submitting a PR:

1. **Keep SKILL.md concise.** Reference superpowers conventions — under 100 lines, flowchart-driven, no verbose tables.
2. **Cross-platform scripts.** Every script needs `.cmd` (Windows) and `.sh` (Linux/macOS) versions.
3. **Never hardcode paths.** Agents discover templates by listing directories. Don't assume what's there.
4. **Describe triggering conditions only.** Skill descriptions start with "Use when..." — never summarize the workflow.
5. **Disclose your model and harness** in the PR description.

## Pull Request Requirements

- One skill or feature per PR
- Verify scripts work on both platforms
- Target `main` branch

## What We Will Not Accept

- Hardcoded template paths in SKILL.md
- Windows-only or Linux-only scripts (unless genuinely platform-specific)
- SKILL.md over 150 lines without justification
- Description fields that summarize workflow instead of triggering conditions

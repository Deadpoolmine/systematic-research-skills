# systematic-research-skills

Systematic Research Skills — A structured research methodology framework for AI coding agents.

## Overview

This project transforms rigorous academic research workflows into executable skill modules for coding agents, ensuring every research task follows a structured, verifiable, and reproducible methodology.

## Supported Platforms

- **Claude Code** — via `.claude-plugin`
- **Cursor** — via `.cursor-plugin`
- **Codex** — via `.codex-plugin`
- **GitHub Copilot** — via instruction files

## Core Principles

- **Systematic over ad-hoc** — Process over guesswork
- **Evidence over claims** — Verify before declaring success
- **Structured decomposition** — Break complex problems into independently verifiable sub-problems
- **Reproducibility** — Every step traceable and reproducible

## Skill Map (Planned)

| Category | Skill | Description |
|----------|-------|-------------|
| Research Prep | Research Question Definition | Clarify scope, goals, and success criteria |
| Literature | Systematic Literature Review | Structured search, screening, and evaluation of existing knowledge |
| Hypothesis | Testable Hypothesis Construction | Build verifiable hypotheses from known knowledge |
| Experiment | Experiment Design | Design reproducible experiments to test hypotheses |
| Data Analysis | Systematic Data Analysis | Structured analysis and conclusion drawing |
| Synthesis | Research Findings Synthesis | Integrate scattered findings into coherent knowledge |
| Peer Review | Research Review | Systematic review of research process and conclusions |

## Project Structure

```
├── skills/              # Skill module directory
├── hooks/               # Session start hooks
├── scripts/             # Utility scripts
├── tests/               # Tests
├── .claude-plugin/      # Claude Code plugin config
├── .codex-plugin/       # Codex plugin config
├── .cursor-plugin/      # Cursor plugin config
└── .github/             # GitHub config
```

## License

MIT License

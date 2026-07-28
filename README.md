# Systematic Research Skills

Agent-driven research methodology toolkit — HLS paper writing and persona-based peer review.

## Core Capabilities

### Paper Writing — Hierarchical Logic Stream (HLS)

4-level top-down refinement for academic writing. Each level validates before descending.

| Level | Role | What It Does |
|-------|------|-------------|
| **L0** | Judge | Pressure-test thesis, determine target venue |
| **L1** | Architect | Design custom Section flow chains |
| **L2** | Builder | Draft/revise Sections in parallel |
| **L3** | Auditor | Cross-validate L0↔L1↔L2 consistency |

Full write mode: **L0 → L1 → L2 → L3**. Polish mode: extract HLS from draft → critical review → L2/L3.

### Paper Review — Persona-Driven Multi-Reviewer Simulation

5 subagents embody distinct reviewers (unique domain, expertise 1-5, research taste) and review in parallel. Each supports interactive QA with persistent memory.

| Step | What It Does |
|------|-------------|
| Casting | Generate 5 diverse reviewer personas |
| Review | 5 subagents review simultaneously (system/AI templates auto-discovered) |
| Dialogue | QA with specific reviewers in character with memory |

### Paper Extract — Reverse HLS Decomposition

Inverse of paper-writing HLS: decomposes existing papers into HLS components for deep understanding, gap identification, and research positioning.

| Phase | Role | Output |
|-------|------|--------|
| **E0** | Extractor | Full text + figures from PDF/LaTeX |
| **E1** | Decomposer | HLS 7+1 core points with evidence |
| **E1.5** | Condenser | TLDR from Abstract+Intro only |
| **E2** | Architect | Section flow chains + dependency graph |
| **E3** | Critic | Innovation, gaps, positioning assessment |

### Paper Plot — Hierarchical Figure Generation

4-level refinement for academic figures — from high-level intent to visual polish, parallel to paper-writing HLS.

| Level | Role | What It Does |
|-------|------|-------------|
| **P0** | Director | Figure intent, type selection, template matching |
| **P1** | Architect | Spatial layout, structured spec + rough draft |
| **P2** | Builder | SVG-first generation, browser preview, PPTX export |
| **P3** | Stylist | 13-point rubric: style, semantics, layout, robustness, consistency |

### Analyze Plot — Skill Improvement via Case Study

Full-loop meta-skill: read paper → generate figure → compare with ground-truth → extract generalizable principles → improve paper-plot. Drives continuous improvement of the paper-plot skill through concrete case studies.

| Phase | Role | Output |
|-------|------|--------|
| **A1** | Reader | System architecture from paper text only |
| **A2** | Generator | Overview figure using current paper-plot principles |
| **A3** | Analyzer | Quantitative gap analysis vs ground-truth |
| **A4** | Abstractor | Paper-agnostic generalizable principles |
| **A5** | Integrator | Skill file diffs to improve paper-plot |

## Skills

| Skill | Description |
|-------|------------|
| [paper-writing](skills/paper-writing/SKILL.md) | HLS-driven paper writing — from core idea to consistency-checked manuscript |
| [paper-review](skills/paper-review/SKILL.md) | Persona-driven peer review simulation with interactive QA |
| [paper-extract](skills/paper-extract/SKILL.md) | Reverse HLS decomposition — extract and analyze papers from PDF/LaTeX |
| [paper-plot](skills/paper-plot/SKILL.md) | Hierarchical figure generation for academic papers (SVG → PPTX) |
| [analyze-plot](skills/analyze-plot/SKILL.md) | Case-study meta-skill — learn figure design principles from ground-truth examples |
| [academic-pptx-skill](skills/academic-pptx-skill/SKILL.md) | Evidence-led academic PPTX generation via HTML/Tailwind authoring and PptxGenJS export |

## Conventions

- **Venue-driven discovery.** Templates auto-discovered by listing directories — never hardcoded.
- **Cross-platform.** All scripts have `.cmd` (Windows) and `.sh` (Linux/macOS) variants.
- **Superpowers-level conciseness.** Hard gates, flowcharts, no verbose tables. SKILL.md under 100 lines.

## Installation

### GitHub Copilot (VS Code)

Clone the repository and open it as a workspace:

```bash
git clone https://github.com/Deadpoolmine/systematic-research-skills.git
```

Skills under `skills/` are auto-discovered by Copilot Chat. For any project, copy the desired skill directories into your project's `skills/` folder.

### Standalone

No dependencies. Skills are self-contained Markdown + scripts. Copy `skills/<name>/` into any project to use.

## Acknowledgments

- [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs/) — Orchestra Research's AI research skill collection
- [research-writing-skill](https://github.com/alfonso0512/research-writing-skill/) — Alfonso's research writing skill for coding agents
- [superpowers](https://github.com/obra/superpowers) — Superpowers-level conciseness conventions for AI agent skills

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CLAUDE.md](CLAUDE.md).

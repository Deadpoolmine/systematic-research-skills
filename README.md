<p align="center">
  <img src="assets/BG.png" alt="Systematic Research Skills" />
</p>

<h1 align="center">Systematic Research Skills</h1>

---

<p align="center">
  <em>We believe research papers are for humans to read. We harness AI to align with human thinking — to sharpen ideas, structure arguments, visualize concepts, and stress-test claims. AI amplifies the researcher, not replaces them.</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License" /></a>
  <a href="https://github.com/Deadpoolmine/systematic-research-skills/stargazers"><img src="https://img.shields.io/github/stars/Deadpoolmine/systematic-research-skills?style=flat&color=EF5A29" alt="GitHub stars" /></a>
  <a href="https://github.com/Deadpoolmine/systematic-research-skills/issues"><img src="https://img.shields.io/github/issues/Deadpoolmine/systematic-research-skills?color=6B625C" alt="Open issues" /></a>
  <a href="https://github.com/Deadpoolmine/systematic-research-skills/graphs/contributors"><img src="https://img.shields.io/github/contributors/Deadpoolmine/systematic-research-skills?color=6B625C" alt="Contributors" /></a>
</p>

## 1. Core Insight

**Hierarchical Logic Stream (HLS) first, top-down research methodology.** Every skill in this toolkit follows a common philosophy: decompose complex research tasks into hierarchical levels (L0→L1→L2→L3), validate at each gate before descending, and produce verifiable, consistency-checked artifacts. From paper writing to figure generation to peer review — HLS is the backbone, top-down refinement is the workflow.

## 2. Core Capabilities

### 2.1 Paper Writing — Hierarchical Logic Stream (HLS)

4-level top-down refinement for academic writing. Each level validates before descending.

| Level | Role | What It Does |
|-------|------|-------------|
| **L0** | Judge | Pressure-test thesis, determine target venue |
| **L1** | Architect | Design custom Section flow chains |
| **L2** | Builder | Draft/revise Sections in parallel |
| **L3** | Auditor | Cross-validate L0↔L1↔L2 consistency |

Full write mode: **L0 → L1 → L2 → L3**. Polish mode: extract HLS from draft → critical review → L2/L3.

### 2.2 Paper Review — Persona-Driven Multi-Reviewer Simulation

5 subagents embody distinct reviewers (unique domain, expertise 1-5, research taste) and review in parallel. Each supports interactive QA with persistent memory.

| Step | What It Does |
|------|-------------|
| Casting | Generate 5 diverse reviewer personas |
| Review | 5 subagents review simultaneously (system/AI templates auto-discovered) |
| Dialogue | QA with specific reviewers in character with memory |

### 2.3 Paper Extract — Reverse HLS Decomposition

Inverse of paper-writing HLS: decomposes existing papers into HLS components for deep understanding, gap identification, and research positioning.

| Phase | Role | Output |
|-------|------|--------|
| **E0** | Extractor | Full text + figures from PDF/LaTeX |
| **E1** | Decomposer | HLS 7+1 core points with evidence |
| **E1.5** | Condenser | TLDR from Abstract+Intro only |
| **E2** | Architect | Section flow chains + dependency graph |
| **E3** | Critic | Innovation, gaps, positioning assessment |

### 2.4 Paper Plot — Hierarchical Figure Generation

4-level refinement for academic figures — from high-level intent to visual polish, parallel to paper-writing HLS.

| Level | Role | What It Does |
|-------|------|-------------|
| **P0** | Director | Figure intent, type selection, template matching |
| **P1** | Architect | Spatial layout, structured spec + rough draft |
| **P2** | Builder | SVG-first generation, browser preview, PPTX export |
| **P3** | Stylist | 13-point rubric: style, semantics, layout, robustness, consistency |

### 2.5 Analyze Plot — Skill Improvement via Case Study

Full-loop meta-skill: read paper → generate figure → compare with ground-truth → extract generalizable principles → improve paper-plot. Drives continuous improvement of the paper-plot skill through concrete case studies.

| Phase | Role | Output |
|-------|------|--------|
| **A1** | Reader | System architecture from paper text only |
| **A2** | Generator | Overview figure using current paper-plot principles |
| **A3** | Analyzer | Quantitative gap analysis vs ground-truth |
| **A4** | Abstractor | Paper-agnostic generalizable principles |
| **A5** | Integrator | Skill file diffs to improve paper-plot |

## 3. Skills

| Skill | Description |
|-------|------------|
| [paper-writing](skills/paper-writing/SKILL.md) | HLS-driven paper writing — from core idea to consistency-checked manuscript |
| [paper-review](skills/paper-review/SKILL.md) | Persona-driven peer review simulation with interactive QA |
| [paper-extract](skills/paper-extract/SKILL.md) | Reverse HLS decomposition — extract and analyze papers from PDF/LaTeX |
| [paper-plot](skills/paper-plot/SKILL.md) | Hierarchical figure generation for academic papers (SVG → PPTX) |
| [analyze-plot](skills/analyze-plot/SKILL.md) | Case-study meta-skill — learn figure design principles from ground-truth examples |
| [academic-pptx-skill](skills/academic-pptx-skill/SKILL.md) | Evidence-led academic PPTX generation via HTML/Tailwind authoring and PptxGenJS export |
| [paper-orchestrator](skills/paper-orchestrator/SKILL.md) | Orchestrate paper projects — inspect state, route to the right specialist, and recheck downstream work |

## 4. Conventions

- **Venue-driven discovery.** Templates auto-discovered by listing directories — never hardcoded.
- **Cross-platform.** All scripts have `.cmd` (Windows) and `.sh` (Linux/macOS) variants.
- **Superpowers-level conciseness.** Hard gates, flowcharts, no verbose tables. SKILL.md under 100 lines.

## 5. Installation

### 5.1 GitHub Copilot (VS Code)

Clone the repository and open it as a workspace:

```bash
git clone https://github.com/Deadpoolmine/systematic-research-skills.git
```

Skills under `skills/` are auto-discovered by Copilot Chat. For any project, copy the desired skill directories into your project's `skills/` folder.

### 5.2 Standalone

No dependencies. Skills are self-contained Markdown + scripts. Copy `skills/<name>/` into any project to use.

## 6. Acknowledgments

- [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs/) — Orchestra Research's AI research skill collection
- [research-writing-skill](https://github.com/alfonso0512/research-writing-skill/) — Alfonso's research writing skill for coding agents
- [superpowers](https://github.com/obra/superpowers) — Superpowers-level conciseness conventions for AI agent skills

## 7. Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CLAUDE.md](CLAUDE.md).

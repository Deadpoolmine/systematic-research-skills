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

## Skills

| Skill | Description |
|-------|------------|
| [paper-writing](skills/paper-writing/SKILL.md) | HLS-driven paper writing — from core idea to consistency-checked manuscript |
| [paper-review](skills/paper-review/SKILL.md) | Persona-driven peer review simulation with interactive QA |

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CLAUDE.md](CLAUDE.md).

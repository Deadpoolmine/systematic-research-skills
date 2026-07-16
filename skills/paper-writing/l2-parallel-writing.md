# L2 — Parallel Writing Stream (The Builder Phase)

**Load when:** executing L2 (write or polish). Writing protocol and skeleton usage.

**REQUIRED BACKGROUND:** SKILL.md hard gates. L1 complete.

## Mode: Write vs Polish

| Mode | Action |
|------|--------|
| **Write** | Copy skeleton → create Sections from scratch → draft |
| **Polish** | Load existing `paper/` → revise each Section following L1 flow chains + writing guide |
| **Polish-lite** | Load draft → use writing guide for voice/pitfalls → revise prose. Do NOT restructure. |

## Checklist

1. **Discover skeleton** — explore `templates/` to find matching format from venue. Read `README.md`. Write: copy to `paper/`. Polish: use existing `paper/`.
2. **Discover writing guide** — `writing-guide.md` in same category. Voice, conventions, per-section pitfalls.
3. **For each L1 Section:** Write: create `paper/sections/<Name>.tex` + `\input` in main.tex. Polish: revise existing file. Draft/review following L1 flow chain AND writing guide.
4. **Execute figure placeholders:** each `[Figure: ...]` → full LaTeX `\begin{figure}...\end{figure}`. Polish: check existing figures match L1 placeholders.
5. **Draft mode:** incomplete experiments → `[TODO: actual number]`. Setup complete.
6. **Self-check** each Section against writing guide pitfalls.
7. **Add references** to `paper/references.bib`.

## Skeleton Rules

- Read-only. Never edit inside `templates/`.
- `sections/` and `figs/` = `.gitkeep` only — fill during L2.
- AAAI: `\input` forbidden → inline in `main.tex`.

## Transition

Commit `paper/` with `L2: draft for <topic>` (or `L2: polish for <topic>`). Proceed to L3.

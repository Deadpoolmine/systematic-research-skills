# General Writing Guide

**Load when:** writing or polishing any academic paper (L2/L3).

---

## Editor Role

- Fix grammar. Leave good prose alone. Never break `\ref{}`, `\cite{}`, `\includegraphics{}`, math mode.
- Match venue tone: precise, evidence-driven, honest about scope. No hand-waving. No marketing.

---

## Overall Voice

- **"we".** Present tense for design; past tense for experiments. Avoid passive.
- **Paragraph:** 3-5 sentences, hard cap 6. One idea = one chain step. Topic → support → conclude. Use `\paragraph{}` to label the topic sentence.
- **Sentence:** 10-25 words, hard cap 30. Open with the point, not context. Vary openings — avoid back-to-back parallel starts.
- **Cut filler verbs:** emerged, enabled, facilitated, leveraged, utilized. ❌ "has emerged as a promising approach" → ✅ "reduces this overhead".
- **One `\ul{}` per section** for the punchline. Kill weak last sentences — the second-to-last is usually the strongest ending.
- **Use plain terms.** If a concept can be expressed with basic words, do so. Abstract domain-jargon signals untranslated ideas.
- **LaTeX comments as scaffolding:** `% reasoning`, `% alternative: X`. Clean before submission.

---

## Introduction Narrative Order

Strict causal chain — never jump ahead. The refined 7-paragraph template:

```
Para 1: Domain context (what field, what capability)
Para 2: Existing approaches (categories, best one identified, underlined)
Para 3: Challenges (only those with strong causal link to root cause)
Para 4: Root cause + key insight (merged, no mechanical "Instead of X..." triplet)
Para 5: Core techniques (address challenges) + bonus technique (additional)
Para 6: System name + headline result
Para 7: Contributions (itemize, one line each)
```

**Key structural rules:**
- Root cause AFTER symptoms. Not "X causes three problems."
- First paragraph = field context only. No method mentions.
- Key insight paragraph states the insight, not the mechanisms — those go in the techniques paragraph.
- Separate core techniques from bonus techniques in the prose. The reader should know which designs answer challenges and which are additional.
- Key insight gets its own contribution bullet. Problem and idea are separate bullets.

**Abstract:** Start from problem landscape, not solution. One sentence per logical step. Match Introduction's terminology. 5 sentences, hard cap 8. No citations, no undefined acronyms. Cut adjectives — state numbers.

---

## Challenge & Technique Patterns

**Challenges:** Each states a mechanism and its consequence — one causal chain. If one sentence suffices, write one. No filler ("concrete," "specifically").

**Core techniques:** Make the link to the challenge explicit — the reader should see which problem each design solves. But vary your sentence structure; don't repeat the same frame mechanically.

**Bonus techniques:** Signal these as additional contributions, not challenge-driven. "We also introduce..." or "Additionally, we propose..." suffices. Don't force a challenge link that doesn't exist.

**Contribution bullets:** One line each, no subordinate clauses. Problem bullet and key-idea bullet are separate — never merge.

---

## Word Choice

| ❌ Avoid | ✅ Use | Note |
|----------|--------|------|
| gap (research/performance) | challenges, limitations, bottlenecks | Name the actual problem |
| leverage (verb) | use, apply | Corporate-speak |
| utilize | use | Never adds meaning |
| facilitate | help, enable | Vague — say how |
| ameliorate / delineate / elucidate | improve / describe / explain | Pretentious |
| heretofore | previously | Archaic |
| efficacy | effectiveness | Clinical-trial language |
| paradigm | approach, method | Overblown |
| a new class of | delete | Filler |
| concrete challenges | challenges | "Concrete" adds nothing |
| design points | designs | Internal terminology |
| instantiates | realizes, achieves | Over-formal |
| plateau (verb) | stall, top out | Jargon |
| closed loop | self-reinforcing cycle / complete workflow | Describe what it does, not that it exists |
| trading off X against Y | state the tradeoff directly | Name what is gained and lost |

## Symbol Hygiene

- **No `---` as causal connector.** ❌ "X exposes Y --- causing Z% degradation." → ✅ split into two sentences, or "X exposes Y, which causes Z% degradation." Allow `---` only for parenthetical asides — prefer commas.
- **No `$\rightarrow$` in prose.** Arrows are for math only. ❌ `A $\rightarrow$ B $\rightarrow$ C` → ✅ "from A to B, then C."
- **No internal notation in text.** Labels like `(DP1 → C1)` are authoring tools — remove them. The mapping should be clear from context.

## List Formatting

- **Inline enumeration:** `First, ... Second, ... Third, ...` with `\emph{italic lowercase}` names. Never bold title case. For long items, use `(1)` / `(2)` / `(3)`.
- **Standalone lists:** `\begin{itemize}`, never `\begin{enumerate}`. No numbers in contribution lists.
- **Contribution bullets:** One line each. No subordinate clauses. The main text already explained everything — the list is a summary index. Problem bullet and key-idea bullet are separate — never combine "we identify X and propose Y." Bonus technique appears in the design bullet but does not need its own contribution line unless independently significant.
- **Cut meaningless lists.** If the sentence works without the enumeration, delete it. "X that A, B, and C" → just "X".

## Terminology

- Named components: **italic lowercase** in prose (`\emph{component name}`). Capitalize only in section titles.
- Category shorthand in parentheses is fine: `category name (C1)`.
- Proper names: capitalize at first definition, lowercase thereafter.

## Specificity

| ✅ | ❌ |
|----|----|
| "85.2% top-1, +1.3 over ViT-B/16." | "Superior performance." |
| "512 GPU-days on 8×A100 (80GB)." | No compute stated. |
| "2.3× higher throughput on workload Y." | "Dramatically outperforms." |
| `% [TODO: actual number]` | `$$[TODO]$$` |

**[TODO] Conventions:** `[TODO: actual number]` as plain text or `%` comment. Never inside `$$`. Use `[TODO: value]` in tables. Keep superseded phrasings as `%` comments.

---

## Figure & Table Templates

### Figure

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=\linewidth]{figs/filename.pdf}
    \caption{\textbf{Bold title.} \small\emph{One-sentence takeaway}.}
    \label{fig:labelname}
\end{figure}
```

- `[t]` default. `[ht]` only if top breaks ordering. **Width: always `\linewidth`.** Use `figure*`/`table*` for double-column spanning.
- Caption: **bold title** + `\small` description. Always state the takeaway.
- **Drafting:** `example-image-a` placeholder (mwe package). Vector PDF/EPS in `figs/`.
- Reference BEFORE it appears: `Figure~\ref{fig:label} shows...` — never "the figure below".

### Table (booktabs only)

```latex
\begin{table}[t]
    \centering
    \caption{\textbf{Table title.} \small\emph{One-sentence takeaway}.}
    \label{tab:labelname}
    \small
    \begin{tabular}{lccc}
        \toprule
        Method & Metric A & Metric B & Avg \\
        \midrule
        Baseline 1 & 72.3 & 68.1 & 70.2 \\
        \textbf{Ours} & \textbf{78.5} & \textbf{73.4} & \textbf{76.0} \\
        \bottomrule
    \end{tabular}
\end{table}
```

- `\toprule`/`\midrule`/`\bottomrule`. Never `\hline`. No vertical rules.
- Bold your method's row. Bold best numbers. `\small` for fitting. `l` for text, `c` for numbers.
- **Ablation:** "Full model" row at top, subtract components below with `\ \ - Component` indent. Show Δ from full.
- Wide tables (5+ columns): `table*`. Draft: `[TODO: value]`.
- **Must-have:** architecture overview (Method) + main results table (Experiments).

| Section | Typical Figures/Tables |
|---------|----------------------|
| Introduction | Teaser/overview (optional) |
| Method | Architecture/pipeline overview (required) |
| Experiments | Main results (required), ablation (required), analysis (2-3) |
| Analysis | Qualitative examples, error cases |

---

## Section Checklists

### Abstract
- [ ] Starts with problem landscape, not solution
- [ ] No `---` or `$\rightarrow$`
- [ ] Italic lowercase for named components
- [ ] Matches Introduction terminology

### Introduction
- [ ] Follows 7-para structure: context → approaches → challenges → root cause+insight → techniques (core+bonus separated) → system+result → contributions
- [ ] No `---`, no `$\rightarrow$` in prose
- [ ] No `instantiates` / `plateau` / `a new class of` / `closed loop`
- [ ] All challenges pass causal test (L0)
- [ ] Core techniques linked to challenges; bonus techniques not forced
- [ ] Contribution bullets: one line each, problem and key-idea separate

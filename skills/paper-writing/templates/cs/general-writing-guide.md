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

Strict causal chain — never jump ahead:

```
Broad domain context
  → Specific sub-area + existing approaches
    → Problems observed (symptoms only, no root cause yet)
      → Root cause (single underlying reason)
        → Key insight (separate paragraph)
          → Method preview (how insight is operationalized)
            → Contributions (one line each)
```

- Root cause AFTER symptoms. "Three problems arise. We find their root cause is X." — not "X causes three problems."
- First paragraph = field context only. No method mentions.
- Key insight deserves its own paragraph and contribution bullet.

**Abstract:** Start from problem landscape, not solution. One sentence per logical step. Match Introduction's terminology. 5 sentences, hard cap 8. No citations, no undefined acronyms. Cut adjectives — state numbers.

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
- **Contribution bullets:** One line each. No subordinate clauses. The main text already explained everything — the list is a summary index.
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
- [ ] `First, ... Second, ... Third, ...` if enumerating
- [ ] Matches Introduction terminology

### Introduction
- [ ] Para 1: Field context only
- [ ] Para 2: Existing approaches
- [ ] Para 3: Problems/symptoms (no root cause yet)
- [ ] Para 4: Root cause
- [ ] Para 5: Key insight (separate paragraph)
- [ ] Para 6: Method preview (italic lowercase, First/Second/Third)
- [ ] Para 7: Contributions (itemize, one line each)
- [ ] No `---`, no `$\rightarrow$` in prose
- [ ] No `instantiates` / `plateau` / `a new class of` / `closed loop`
- [ ] No meaningless enumerations
- [ ] All lists: `First, ...` + `\emph{lowercase}` or `itemize`

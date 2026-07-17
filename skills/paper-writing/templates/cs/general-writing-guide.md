# General Writing Guide

**Load when:** writing or polishing any academic paper (L2/L3). Covers voice, vocabulary, paragraph/sentence rules, natural language conventions, and LaTeX figure/table templates.

---

## Editor Role

Act as an academic editor. Make prose precise, evidence-driven, and venue-appropriate — not rewrite for the sake of rewriting.

- **Correct grammar errors.** Fix what's wrong. Leave good prose alone.
- **Preserve LaTeX.** Never break `\ref{}`, `\cite{}`, `\includegraphics{}`, math mode.
- **Match venue tone.** Precise, evidence-driven, honest about scope. No hand-waving. No marketing.

---

## Overall Voice

- **"we".** Present tense for design; past tense for experiments. Avoid passive.
- **Precise.** Define notation before use. Every equation explained in prose. Numbers have units. Claims name baseline + metric.
- **Honest.** Acknowledge limitations concretely. State compute. "On 3 benchmarks" not "state-of-the-art."
- **Paragraph:** 3-5 sentences, hard cap 6. One idea = one chain step = at least one paragraph.
- **Sentence:** 10-25 words, hard cap 30 words. Split long sentences at nearest clause boundary.
- **Paragraph structure:** Topic sentence → 2-3 supporting sentences → concluding/transition. First sentence declares the point. Use `\paragraph{}` to label and summarize the topic sentence.
- **Open with the point, not the context.** ❌ "The growing use of... has created increasing demand for..." → ✅ "X relies on Y."
- **Cut setup verbs.** ❌ "has emerged as a promising approach" → ✅ "reduces this overhead". Verbs that add syllables without meaning: emerged, enabled, facilitated, leveraged (as verb).
- **Underline the punchline.** One `\ul{}` per section marks the finding everything else supports.
- **Kill the last sentence.** Most paragraphs end with a weak restatement. The second-to-last sentence is usually the strongest ending.
- **Use LaTeX comments as scaffolding.** `% reasoning`, `% alternative: X`, `% TODO: verify number`. Clean before submission.
- **Define notation before use.** Evidence-backed claims. Specific > vague.

---

## Natural Language Conventions

These rules keep prose sounding like a human wrote it — not a template.

### Banned Words & Replacements

| ❌ Banned | ✅ Use Instead | Why |
|-----------|---------------|-----|
| gap (as in "research gap", "performance gap") | challenges, existing problems, limitations, bottlenecks, unsolved issues | "Gap" is overused template-speak. Name the actual problem. |
| --- (em dash for causal connection) | rewrite as two sentences, or use "—" sparingly for parenthetical asides only | Em dash chaining makes prose feel breathless and formulaic. Prefer clear sentence boundaries. |
| closed loop | that form an efficient, effective XX approach; a self-reinforcing cycle; a complete workflow | "Closed loop" is jargon. Describe what the loop actually achieves. |
| paradigm | approach, method, framework | Overblown. |
| leverage (as verb) | use, apply, exploit, take advantage of | Corporate-speak. |
| utilize | use | "Utilize" never adds meaning over "use". |
| facilitate | help, enable, support | Vague. Say how. |
| ameliorate | improve, reduce, cut | Pretentious. |
| delineate | describe, outline | Pretentious. |
| elucidate | explain, show | Pretentious. |
| heretofore | previously, so far | Archaic. |
| efficacy | effectiveness | "Efficacy" is clinical-trial language. |

### Abstract Rules

- **5 sentences, hard cap 8.** Formula: (1) problem + why it matters → (2) key challenge or existing problem → (3) core insight → (4) what you built + how it works → (5) main result + impact.
- **No citations in abstract** unless venue requires it.
- **No undefined acronyms.**
- **Match the intro's funnel** — same insight wording, same contribution framing.
- **Cut adjectives.** "Extensive experiments" → state the number of benchmarks. "Significant improvements" → state the numbers.

### Em Dash Policy

- **Avoid `---` as a causal connector.** ❌ "X directly exposes Y --- bringing up to Z% degradation." → ✅ "X directly exposes Y, which causes up to Z% degradation." Or split: "X directly exposes Y. This brings up to Z% degradation."
- **Allow `---` only for parenthetical asides** (like this one), and even then, prefer commas or parentheses.
- **Never chain multiple em dashes** in one paragraph.

### "Closed Loop" Replacement Pattern

- ❌ "X and Y form a closed loop." / "This creates a closed-loop system."
- ✅ "X and Y form an efficient, self-reinforcing approach: X improves Y, and the improved Y in turn refines X."
- ✅ "This creates a complete workflow where each component feeds into the next."
- **Rule:** Always explain what the loop *does*, not just that it exists.

### Vocabulary

| ✅ | ❌ |
|----|----|
| show, find, build, measure, cut, eliminate | ameliorate, delineate, elucidate, utilize, leverage |
| improve | ameliorate |
| describe | delineate |
| explain | elucidate |
| previously | heretofore |
| use | utilize, leverage (as verb) |
| help | facilitate |
| reduce | mitigate |
| approach | paradigm |
| effectiveness | efficacy |

### Specificity

| ✅ | ❌ |
|----|----|
| "85.2% top-1 on ImageNet, +1.3 over ViT-B/16." | "Superior performance." |
| "512 GPU-days on 8×A100 (80GB)." | No compute stated. |
| "2.3× higher throughput than baseline on workload Y." | "Dramatically outperforms existing solutions." |
| "After 1000 random crash tests, system recovered from all." | "System is crash-consistent." |
| `% [TODO: actual number]` | `$$[TODO]$$` |
| "degrades on fine-grained classes (Table 5)." | "ameliorates the delineated challenges." |

### [TODO] Conventions

- `[TODO: actual number]` as plain text or `% [TODO: ...]` LaTeX comment.
- **NEVER** inside `$$` or `$`.
- Draft numbers in tables: `[TODO: value]`.
- Iteration traces: keep superseded phrasings as `%` comments. Final text only; traces document refinement.

---

## Figure & Table Templates

Use these templates exactly — do NOT invent alternative styles.

### Single-Column Figure

Use for: architecture overview, pipeline diagrams, method illustrations. Placed at top of column.

```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=\linewidth]{figs/filename.pdf}
    \caption{\textbf{Caption title.} \small Description of what the figure shows and the key takeaway.}
    \label{fig:labelname}
\end{figure}
```

**Rules:**
- `[t]` placement by default. Use `[ht]` only if top placement causes ordering issues.
- **Width: always `\linewidth`.** Single-column → `figure`/`table`; double-column spanning → `figure*`/`table*`.
- Caption: **bold title** + `\small` description. Always state the takeaway, not just "Architecture of X."
- **Drafting:** Use `example-image-a` (mwe package) as placeholder. Replace with real figures before submission.
- Figure file: vector PDF/EPS in `figs/`. Name descriptively: `figs/architecture-overview.pdf`.

---

## Double-Column Figure (Spanning)

Use for: wide tables, large result charts, overview figures in two-column venues.

```latex
\begin{figure*}[t]
    \centering
    \includegraphics[width=\linewidth]{figs/filename.pdf}
    \caption{\textbf{Caption title.} \small Description of what the figure shows and the key takeaway.}
    \label{fig:labelname}
\end{figure*}
```

**Rules:** Same as single-column. Use `figure*` (not `figure`) for full-page-width content.

---

## Table

Use for: main results, ablation studies, dataset statistics. Always use `booktabs` style — no vertical lines.

```latex
\begin{table}[t]
    \centering
    \caption{\textbf{Table title.} \small Description of what this table demonstrates.}
    \label{tab:labelname}
    \small
    \begin{tabular}{lccc}
        \toprule
        Method & Metric A & Metric B & Avg \\
        \midrule
        Baseline 1 & 72.3 & 68.1 & 70.2 \\
        Baseline 2 & 74.1 & 70.2 & 72.2 \\
        \textbf{Ours} & \textbf{78.5} & \textbf{73.4} & \textbf{76.0} \\
        \bottomrule
    \end{tabular}
\end{table}
```

**Rules:**
- `booktabs` package required: `\toprule`, `\midrule`, `\bottomrule`. Never `\hline`.
- **No vertical rules** (`|` in tabular). No double rules.
- Bold your method's row. Bold best numbers in each column.
- `\small` for fitting. Use `\footnotesize` only if desperate.
- Column alignment: `l` for text (left), `c` for numbers (center), `r` only for right-aligned numbers in specific contexts.
- Ablation tables: add a row "Full model" at top, then subtract components. Show delta (Δ) from full model.
- Draft mode: use `[TODO: value]` for unknown numbers.

### Ablation Table Pattern

```latex
\begin{table}[t]
    \centering
    \caption{\textbf{Ablation study on X.} \small We remove each component and report the performance drop.}
    \label{tab:ablation}
    \small
    \begin{tabular}{lcc}
        \toprule
        Configuration & Accuracy & $\Delta$ \\
        \midrule
        Full model (Ours) & 78.5 & — \\
        \ \ - Component A & 75.1 & -3.4 \\
        \ \ - Component B & 73.2 & -5.3 \\
        \ \ - Component C & 76.8 & -1.7 \\
        \bottomrule
    \end{tabular}
\end{table}
```

### Wide Table (Double-Column)

```latex
\begin{table*}[t]
    \centering
    \caption{\textbf{Wide comparison.} \small ...}
    \label{tab:wide}
    \small
    \begin{tabular}{lcccccc}
        \toprule
        Method & Dataset 1 & Dataset 2 & Dataset 3 & Dataset 4 & Dataset 5 & Avg \\
        \midrule
        ... \\
        \bottomrule
    \end{tabular}
\end{table*}
```

---

## Figure/Table Placement by Section

| Section | Typical Figures/Tables |
|---------|----------------------|
| **Introduction** | Figure 1: teaser/overview (optional, venue-dependent) |
| **Method** | Figure 2+: architecture/pipeline overview (required) |
| **Experiments** | Main results table (required), ablation table (required), analysis figures (2-3) |
| **Analysis** | Qualitative examples, error cases, attention maps |

**Must-have figures:** architecture overview (Method) + main results (Experiments). Everything else = if the story needs it.

---

## Cross-Referencing

- Reference BEFORE the figure appears: `Figure~\ref{fig:label} shows...`
- Never: "the figure below" or "the following figure" — use `\ref{}`.
- Tables: `Table~\ref{tab:label}`.

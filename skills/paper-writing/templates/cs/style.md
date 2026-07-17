# Writing Style Reference

**Load when:** writing or polishing any academic paper (L2/L3). Covers voice, vocabulary, paragraph/sentence rules, and LaTeX figure/table templates.

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
- **Em dash for causal connection.** `---` in LaTeX: "X directly exposes Y --- bringing up to Z% degradation."
- **Underline the punchline.** One `\ul{}` per section marks the finding everything else supports.
- **Kill the last sentence.** Most paragraphs end with a weak restatement. The second-to-last sentence is usually the strongest ending.
- **Use LaTeX comments as scaffolding.** `% reasoning`, `% alternative: X`, `% TODO: verify number`. Clean before submission.
- **Define notation before use.** Evidence-backed claims. Specific > vague.

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
    \includegraphics[width=\textwidth]{figs/filename.pdf}
    \caption{\textbf{Caption title.} \small Description of what the figure shows and the key takeaway.}
    \label{fig:labelname}
\end{figure}
```

**Rules:**
- `[t]` placement by default. Use `[ht]` only if top placement causes ordering issues.
- `\textwidth` for full column width. Use `0.95\textwidth` if caption needs breathing room.
- Caption: **bold title** + `\small` description. Always state the takeaway, not just "Architecture of X."
- Figure file: vector PDF/EPS. Place in `figs/`. Name descriptively: `figs/architecture-overview.pdf`.

---

## Double-Column Figure (Spanning)

Use for: wide tables, large result charts, overview figures in two-column venues.

```latex
\begin{figure*}[t]
    \centering
    \includegraphics[width=\textwidth]{figs/filename.pdf}
    \caption{\textbf{Caption title.} \small Description of what the figure shows and the key takeaway.}
    \label{fig:labelname}
\end{figure*}
```

**Rules:** Same as single-column. Use `figure*` (not `figure`). In AAAI/ICLR `\textwidth` = full page width.

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

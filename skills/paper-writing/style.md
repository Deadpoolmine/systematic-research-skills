# LaTeX Figure & Table Style Reference

**Load when:** inserting figures or tables in L2 or L3. Use these templates exactly — do NOT invent alternative styles.

---

## Single-Column Figure

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

# AI Paper Writing Guide

**Load this reference when:** writing or polishing an AI/ML paper. Provides conventions, voice guidance, and common pitfalls for ML venues (NeurIPS, ICML, ICLR, CVPR, ACL, AAAI, etc.).

**Relationship to L1:** The sections below describe **typical writing conventions** for common section types. The actual section structure is determined in L1 through discussion with the user — not copied from this guide. If L1 produces a section not listed here, apply the overall voice principles and adapt from the closest matching section.

---

## Overall Voice

- **Technical precision.** Define notation before use. Every symbol in an equation must be explained in prose. State assumptions explicitly.
- **Evidence-driven.** Claims are backed by experiments, ablations, or theoretical analysis. Avoid hand-waving about "learning meaningful representations."
- **Honest about scope.** A method that works on 3 datasets is not "state-of-the-art across all benchmarks." A method that requires 8×A100s should say so.
- **First person** ("we") is standard.
- **Paragraph structure.** Topic sentence → 2-4 supporting sentences → concluding/transition sentence (总分总). Minimum: topic → support (总分). First sentence = what this paragraph argues. Last sentence = why it matters or what comes next.
- **Paragraph length.** 3-5 sentences. Never exceed 8. Short paragraphs > wall-of-text. One idea per paragraph.
- **Vocabulary.** Standard ML terminology. No obscure words ("ameliorate", "delineate", "elucidate", "heretofore", "aforementioned", "thusly"). Use plain English: "improve" not "ameliorate", "describe" not "delineate", "explain" not "elucidate".
- **Blueprint is binding.** The section structure, paragraph count, and page budget from the blueprint are HARD constraints — not suggestions. Every paragraph must serve the blueprint's specified purpose.
- **`[TODO]` markers:** Use `% [TODO: actual number]` as a LaTeX comment, or inline text like `[TODO: actual number]`. NEVER wrap in `$$` or `$`. Math mode renders TODO as an equation — wrong.

| ✅ Good | ❌ Bad |
|---------|--------|
| "On ImageNet-1K, our method achieves 85.2% top-1 accuracy, a 1.3 point improvement over ViT-B/16 (83.9%)." | "Our method achieves superior performance." |
| "Training requires 512 GPU-days on 8×A100 (80GB)." | (no compute requirements mentioned) |
| "The improvement is most pronounced on long-tail classes (Figure 4), suggesting the auxiliary loss regularizes rare categories." | "The auxiliary loss helps." |
| `% [TODO: actual number]` or `[TODO: actual number]` | `$$[TODO: actual number]$$` (never math mode!) |
| "While effective, our method degrades on fine-grained classes (Table 5)." | "Our method ameliorates the delineated challenges heretofore unaddressed." |

---

## Introduction

### Purpose
Establish the task, identify the gap in current methods, present your insight, preview results.

### Structure (1-1.5 pages max)

| Step | Sentences | Content |
|------|-----------|---------|
| Big Background | 2-3 | Name the AI trend. Specific scale + recency. |
| Small Background | 2-3 | Narrow to task. Cite 2-3 SOTA works. |
| Gap | 3-4 | What SOTA misses + evidence + root cause. **Most critical step.** |
| Key Idea | 2-3 | ONE insight. Why it works, not what you built. |
| Method Preview | 3-4 | 2-3 contributions, 1 sentence each. Tie to key idea. |
| Experiment Summary | 2-3 | Benchmarks + baselines + headline number. |

**Contributions (bullet list):** 2-3 bullets max. One line each. Conceptual (insight) vs technical (method). No sub-bullets.

### Pitfalls
- Generic opening ("Recently, there has been growing interest in...")
- Claiming SOTA without naming the benchmark
- Method preview = table of contents ("Module A, then B, then C") — connect to WHY
- Overclaiming ("We solve X")

---

## Related Work

### Purpose
Position your work. Group by theme. Be fair and specific about how you differ.

### Structure & Advice

**Thematic grouping:** 3-4 categories. Examples: "Efficient Transformers", "Contrastive Learning for Vision", "Diffusion-Based Generation." For each:
1. Key works and their contributions (2-3 sentences per work)
2. Collective limitations of this line of work
3. How your work differs (explicit comparison)

**Be gracious.** The authors of cited papers may be your reviewers. "While X achieves strong results, it requires..." not "X fails to..."

### Pitfalls
- The "laundry list" — paragraph after paragraph of "X did A, Y did B, Z did C" with no synthesis
- Missing recent preprints (reviewers check arXiv)
- Unfair comparisons ("Unlike prior work, our method doesn't require X" when prior work never claimed to need X)

---

## Preliminaries

### Purpose
Provide the necessary background to understand your method. Not a textbook chapter.

### Structure & Advice

**Problem formulation:** Formal definition of input space X, output space Y, objective function L. This is the contract for the rest of the paper.

**Notation table:** Define every symbol used in equations. Consistent throughout the paper.

**Background concepts:** Explain only what's needed. If your method builds on attention — explain attention in 3 sentences, cite Vaswani et al., and move on. If you extend a specific prior method, summarize it here so the reader can understand your changes.

### Pitfalls
- Tutorial-level explanations of well-known concepts (wastes space, annoys expert reviewers)
- Notation that conflicts with standard usage in the community
- Missing definitions for symbols that appear in equations

---

## Method

### Purpose
The intellectual core. The reader should be able to re-implement from this section alone.

### Structure & Advice

**Overview (1 paragraph + figure):** Pipeline diagram. Walk through end-to-end: input → component A → component B → output. The diagram should tell the story at a glance.

**Each component (one subsection each):** For every technical contribution:
1. **Motivation** — why is this component needed? (1 sentence)
2. **Mechanism** — how does it work? Equations, algorithms, architecture diagrams
3. **Why this design** — what alternatives were considered and rejected?
4. **Connection to key idea** — explicitly state how this serves the L0 key idea

**Equations:** Every equation must be explained in the surrounding prose. Variables defined before use. The prose tells WHY; the equation formalizes.

**Algorithms:** Use `algorithm` + `algorithmic` packages. Algorithm is self-contained but accompanied by prose that explains the intuition. Line numbers for referencing.

**Training/inference details:** Loss function, optimizer, learning rate schedule, hyperparameters. These can go here or in Experiments setup — be consistent.

### Pitfalls
- Equations without surrounding prose explanation
- Components that don't connect to the key idea
- Architecture described only in text without a figure
- Hyperparameters buried in appendix that are critical to understanding the method

---

## Experiments

### Purpose
Prove your method works. Show when, by how much, and why.

### Structure & Advice

**Setup:** Reproducibility is paramount. Include:
- Dataset statistics (size, splits, preprocessing)
- Baseline descriptions and configurations (how were they tuned?)
- Evaluation metrics (why these metrics?)
- Implementation details (hardware, libraries, hyperparameters, random seeds)
- Compute budget for training (GPU-hours, hardware type)

**Main results:** Headline table or figure. Compare against baselines. For each comparison:
- WHAT is the difference?
- WHY does the difference exist? (not just "our method is better")
- Is the difference statistically significant? (standard deviation, significance tests)

**Ablation studies:** Remove each component, measure the drop. This proves your components matter. An ablation table should show:
- Full model performance
- Model minus component 1
- Model minus component 2
- Model minus component 3
- Summary: which components contribute most?

**Analysis:** Go beyond numbers:
- Qualitative examples (visualizations, case studies)
- Error analysis (when does your method fail? show examples)
- Efficiency analysis (inference time, memory, parameter count)
- What does the model learn? (attention maps, latent space visualization, probing)

**Draft mode:** If experiments are incomplete, use `[TODO: actual number]`. Setup, baselines, and ablation structure must be fully specified. Expected trends stated.

### Pitfalls
- No standard deviations / error bars
- Ablations that only remove one component at a time (deceptively small drops)
- Cherry-picking the best checkpoint for the main table without describing the selection protocol
- Qualitative examples that only show successes
- Missing compute budget (increasingly required at major venues)

---

## Discussion

### Purpose
Honest reflection. What are the limits? What's next?

### Advice
- **Limitations:** Be specific. "Requires 8×A100 GPUs for training" not "computationally expensive." "Assumes access to paired image-text data" not "data requirements are high."
- **Failure modes:** When doesn't it work? Show a concrete example.
- **Broader impact:** (Optional, required at some venues) Potential misuse, bias considerations, environmental impact of compute.
- **Future work:** 2-3 concrete directions that naturally extend this work.

### Pitfalls
- Vague limitations ("may not generalize") — be specific about which distribution shift
- No limitations section (reviewers will find them for you)
- Future work that reads like a different paper entirely

---

## Conclusion

### Purpose
Remind the reader what they learned. No new information.

### Structure
1. Task and gap (1 sentence)
2. Key insight (1 sentence)
3. What you proposed (1 sentence)
4. Key result (1 sentence)
5. Closing (1 sentence — optional)

### Pitfalls
- Introducing new claims
- Repeating the abstract
- "Future work includes..." (belongs in Discussion)

---

## Polishing Checklist

When polishing an AI paper draft, check:

- [ ] Every equation variable is defined in prose before or immediately after the equation
- [ ] Every figure/table is referenced in the text BEFORE it appears
- [ ] All `[TODO]` placeholders are resolved or explicitly marked as known gaps
- [ ] Hyperparameters are in one place (either Method or Experiments, not scattered)
- [ ] Baseline comparisons are fair (same data splits, same compute budget, proper tuning)
- [ ] Claims are calibrated to evidence ("improves" not "solves"; "on these 3 benchmarks" not "universally")
- [ ] Notation is consistent between Preliminaries, Method, and Experiments
- [ ] Ablation studies isolate individual contributions
- [ ] Limitations are specific, not generic

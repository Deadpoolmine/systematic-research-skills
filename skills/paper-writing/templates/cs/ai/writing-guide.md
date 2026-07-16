# AI Paper Writing Guide

**Load when:** writing/polishing AI/ML papers (NeurIPS, ICML, ICLR, CVPR, ACL, AAAI, COLM).

---

## Overall Voice

- **Precision.** Define notation before use. Every equation explained in prose. State assumptions.
- **Evidence-driven.** Claims backed by experiments/ablations/theory. No "learns meaningful representations."
- **Honest scope.** "On 3 benchmarks" not "state-of-the-art." State compute requirements.
- **"we"**. First person standard.
- **Paragraph structure.** Topic → 2-3 support → conclude/transition (总分总). One idea = one chain step.
- **Paragraph length.** 3-5 sentences. Hard cap: 6. Sentence hard cap: 30 words.
- **Vocabulary.** Plain English. No: ameliorate, delineate, elucidate, heretofore, utilize, leverage.
- **`[TODO]`**: `% [TODO: ...]` as LaTeX comment or plain text. NEVER inside `$$` or `$`.
- **Blueprint is binding.** Section structure + paragraph count + page budget are HARD constraints.

| ✅ | ❌ |
|----|----|
| "85.2% top-1 on ImageNet, +1.3 over ViT-B/16." | "Superior performance." |
| "512 GPU-days on 8×A100 (80GB)." | No compute stated. |
| `% [TODO: actual number]` | `$$[TODO]$$` |
| "degrades on fine-grained classes (Table 5)." | "ameliorates the delineated challenges." |

---

## Introduction (1-1.5pg max)

| Step | Sents | Rule |
|------|-------|------|
| Big Background | 2-3 | Trend + scale + recency. |
| Small Background | 2-3 | Task + SOTA. Cite 2-3 works. |
| Gap | 3-4 | What SOTA misses + evidence + root cause. |
| Key Idea | 2-3 | ONE insight. Why it works. |
| Method Preview | 2-3 | Connect insight to approach. |

**Contributions (END of Intro):** 2-3 bullets, 1 line each. Pattern: (1) Identify problem → (2) Propose insight/technique → (3) Demonstrate results. Optional: Paper Organization (1-2 sentences) after contributions.

**Pitfalls:** Generic opening. SOTA claim without benchmark. Method preview = TOC. Overclaiming.

## Related Work

Group by theme (3-4 categories). Per category: key works → collective limits → how you differ. Be gracious — authors may be reviewers. No laundry lists.

## Preliminaries

Only what's needed. Problem formulation + notation + essential background. Not a textbook. Cite and move on.

## Method

**Must:** architecture overview figure. Per component: motivation (1 sent) → mechanism → why this design → connection to key idea. Equations explained in prose. Variables defined before use. Training details in one place.

**Pitfalls:** Equations without prose. Components not tied to key idea. No architecture figure.

## Experiments

**Setup:** datasets, baselines (how tuned?), metrics (why?), hardware, hyperparams, seeds, compute budget.
**Main results:** what differs + why + statistical significance. **Ablations:** full model minus each component.
**Analysis:** qualitative examples, error cases, efficiency, what the model learns.
**Draft:** `[TODO: number]`. Setup/baselines/methodology fully specified.

**Pitfalls:** No error bars. Cherry-picking. Only showing successes. Missing compute budget.

## Discussion and Limitations

Be specific: "Requires 8×A100" not "computationally expensive." Concrete failure mode. 2-3 future directions.

## Conclusion

5 sentences: task+gap → insight → proposal → result → closing. No new claims. No "Future work" (→ Discussion).

---

## Checklist

- [ ] Every equation variable defined in prose
- [ ] Figures/tables referenced BEFORE they appear
- [ ] All `[TODO]` resolved or marked
- [ ] Hyperparams in one place
- [ ] Fair baselines (same splits, compute, tuning)
- [ ] Claims calibrated: "improves on 3 benchmarks" not "solves"
- [ ] Notation consistent across sections
- [ ] Ablations isolate individual contributions
- [ ] Limitations specific, not generic

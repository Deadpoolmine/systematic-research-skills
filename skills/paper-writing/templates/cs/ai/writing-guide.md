# AI/ML Paper Writing Guide

**Load when:** writing/polishing AI/ML papers (NeurIPS, ICML, ICLR, CVPR, ACL, AAAI, COLM).

**General voice, vocabulary, and style rules:** see [general-writing-guide.md](../general-writing-guide.md). This guide covers **AI/ML-specific** writing patterns only.

---

## AI-Specific Introduction Patterns

Funnel: **big background → small background → challenges / existing problems → insight → design preview → contributions** (1-1.5pg max).

| Step | Rule |
|------|------|
| Big Background | Name the trend. Specific, not generic. Cite 2-3. |
| Small Background | Narrow to your domain. Name the approach category. |
| Challenges | Problem (1 sent) + quantitative evidence + root cause. Name the actual problem, not "gap". |
| Key Insight | ONE insight. Why it works, not what you built. |
| Design Preview | 2-3 design points, 1-2 sentences each. Name the method. |
| Contributions | 2-3 bullets. Pattern: (1) identify problem → (2) propose technique → (3) demonstrate results. |

**AI-specific patterns:**

- **Two-sentence opening.** Avoid "X has achieved remarkable success." Start: what problem + why it matters NOW.
- **"Fortunately" pivot.** After stating the challenges: "Fortunately, our observations show that neither overhead should be paid: (1)... (2)..." Turns problem into opportunity.
- **Encapsulate insights.** "We encapsulate our findings into **N core insights**: (1)... (2)..." Keep the SAME insights verbatim across abstract, intro, and conclusion.
- **Place diagnostic figures early.** Right after abstract or within intro. Visual evidence before method.
- **Classify prior work.** "Existing approaches follow N directions. The first... The second..." — positions your contribution in the design space.
- **Contributions label.** Precede with "In summary, this paper makes the following contributions:"

**Pitfalls:** Generic opening. SOTA claim without benchmark. Method preview = TOC. Overclaiming. Inconsistent insight wording across sections.

---

## Background & Motivation

**Background:** Only what's needed. Define key terms concisely. No textbook.

**Motivation — earn the right to propose a solution:**

- **Named observations.** Label each: `Observation #1:` or `Motivation 1.` Each: quantitative evidence → implication for design.
- **Controlled experiment for root cause.** When degradation has multiple possible causes, isolate each with a variant that changes only one factor. Measure which dominates.
- **Concrete case study.** One representative failure example → quantify mismatch with a diagnostic metric → bold root-cause sentence → explain why existing methods fail → pivot to new objective.
- **Ideal baseline.** Include a theoretical upper bound to make the existing limitations concrete.
- **Insight formalization.** Name the insight memorably. Support with a predictive-power figure (correlation between your proxy and ground truth). Enumerate advantages: ①, ②.
- **End with challenges.** Close with: "Nevertheless, building X is non-trivial, as reflected in N questions: (1)... (2)... We address these in the next section." Bridges to method.

**Pitfalls:** Vague "existing methods are suboptimal." Textbook exposition. No quantitative diagnostic. Insight not tied to a structural invariant. No challenges bridge.

---

## Method

### Organization Patterns

Pick one that fits your method:

- **Challenge-driven.** State N challenges at section start. Each subsection addresses one. Gives reviewers a roadmap.
- **Pipeline-driven.** Overview → Data Preparation → Component 1/2/3 (each: what → features → training) → Implementation.
- **Progressive unveiling.** Present variants incrementally: "Our first attempt was X. However... We thus propose Z." Shows design rationale.

### Formula Derivation Chain (AI-specific)

When method involves a mathematical objective:

1. **Define the loss.** From first principles.
2. **Derive the ideal.** State optimal — even if intractable.
3. **Bound or approximate.** Inequalities to tractable form.
4. **Sensitivity analysis.** Empirically compare candidate proxies via a figure.
5. **Adopt the practical proxy.** Observable quantity that best approximates the ideal.

**Equation rules:** variable defined in prose before/after first use → purpose sentence before equation → interpretation sentence after → `\begingroup\scriptsize` for long derivations.

**Pitfalls:** Equations without prose. Components not tied to key insight. No architecture figure. Skipping sensitivity analysis.

---

## Experiments (ML-Specific)

1. **Questions-driven opening.** "We seek to answer N questions: (1)... (2)... (3)..." Each anchors a subsection.
2. **Setup** (before any results): testbed (HW + SW versions), models, benchmarks, baselines (explain missing ones), seeds, hyperparams, metric definitions.
3. **Main results.** Headline + why wins + why loses. Cross-model, cross-dataset.
4. **Efficiency.** Memory, latency, throughput — three separate dimensions. Explain *why* overhead is small.
5. **Ablations.** Order by fundamentality: (1) core design choice (use oracle/idealized setting to isolate) → (2) component variants (architecture trade-off figure) → (3) hyperparameter sweep.
6. **Sensitivity.** Vary key parameters. Show robustness via convergence curves.

**Pitfalls:** No error bars. Cherry-picking. Graphs without WHY. Missing baselines or their configs. Single-model claimed as general. Ablations that don't isolate.

---

## Related Work

- **Opening:** "To the best of our knowledge, [Method] is the first to [unique contribution]."
- **Structure:** 3-4 thematic categories. Per category: what existing work does → how you differ.
- **End with positioning.** One sentence: "This paper aims to advance X for Y."
- **Be fair.** Authors may be reviewers. No paper dumps — group and compare.
- **Merge with Discussion when space is tight.** `\section{Related Works and Discussion}`.

---

## Discussion & Conclusion

- **Limitations:** Be concrete. "Requires 8×A100" not "computationally expensive." Concrete failure mode. Distinguish design vs. implementation limits. Pre-empt "what about X?" by naming X.
- **Conclusion:** 5 sentences max: problem → insight → what built → key result → closing. No new claims. No bullet points. No "Future work." Reiterate key insights verbatim from abstract and intro.

---

## Checklist

- [ ] Every equation variable defined in prose
- [ ] Key insights verbatim-identical in abstract, intro, conclusion
- [ ] Motivation: concrete observations or controlled experiments with diagnostic metrics
- [ ] Each derivation-chain equation: purpose before, interpretation after
- [ ] Evaluation opens with explicit research questions
- [ ] Cross-model + cross-dataset robustness demonstrated
- [ ] Design choice justified (sensitivity analysis or trade-off figure, not assertion)
- [ ] Ablations isolate individual contributions
- [ ] Fair baselines (same splits, compute, tuning)
- [ ] Claims calibrated: numbers + baseline, not adjectives
- [ ] Limitations concrete, not generic
- [ ] Figure 1 self-contained; every figure caption states conclusion
- [ ] Challenges paragraph bridges motivation to method


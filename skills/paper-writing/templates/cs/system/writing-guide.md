# System Paper Writing Guide

**Load when:** writing/polishing systems papers (OSDI, SOSP, EuroSys, ASPLOS, ATC, FAST, NSDI, SIGMOD).

**General voice, vocabulary, and style rules:** see [general-writing-guide.md](../general-writing-guide.md). This guide covers **systems-specific** writing patterns only.

---

## System-Specific Introduction Patterns

Funnel: **big background → small background → challenges / existing problems → insight → design preview → contributions** (1-1.5pg max).

| Step | Rule |
|------|------|
| Big Background | Name the trend. Specific, not generic. Cite 2-3. |
| Small Background | Narrow to your domain. Name the system category. |
| Challenges | Problem (1 sentence) + quantitative evidence + root cause. Name the actual problem, not "gap". |
| Key Insight | ONE insight. "X merges with Y, eliminating Z." Not "we built X." |
| Design Preview | 2-3 design points, 1-2 sentences each. Name the system. |
| Contributions | 2-3 bullets. Pattern: (1) identify problem → (2) propose technique → (3) demonstrate results. |

**System-specific patterns:**

- **Classify prior work.** "Existing systems follow two approaches. The first kind... The second kind..." — positions your contribution in the design space.
- **Separate model from system.** Give the abstraction a name distinct from the prototype (e.g., "Model X" is the concept; "System Y" is the implementation).
- **State design goals upfront.** 2-3 enumerated goals before presenting the system.
- **Economic motivation.** If applicable, open with a cost table (hardware $/GiB).

**Pitfalls:** Generic opening. Laundry-list contributions (>3 bullets). Hiding insight behind system description. Vague problem statement without numbers.

---

## Background & Motivation

**Background:** Only what's needed. Define key terms concisely. No textbook teaching.

**Motivation — earn the right to propose a solution:**

- **Named observations.** Label each finding: `Observation #1:` or `Motivation 1.` Each has quantitative evidence → implication for design.
- **Ideal baseline.** Include a theoretical upper bound to make the existing limitations concrete.
- **Real hardware, real workloads.** State platform and config even in motivation.
- **Quantify everything.** Not "X is slow" but "X suffers Y% throughput loss at Z workload."
- **Show breakdowns.** A stacked bar of where time goes reveals the true bottleneck.
- **Two-layer structure (optional).** "Understanding X" (broad measurement) → "Analyzing X" (root cause drill-down). Bridge: "This raises one question: *why does X happen?*"

**Pitfalls:** Textbook exposition. No Ideal baseline. Hand-waving. Charts without prose.

---

## Design (System-Specific Patterns)

### Goals-to-Techniques Mapping

After Architecture Overview, add a paragraph explicitly mapping each technique to each design goal. Reviewers check this.

### Key Patterns

- **Operation-to-abstraction table.** Map N operations to M primitives in a table (columns: Op, Primitive, How). Proves completeness without enumerating in prose.
- **Progressive unveiling.** For multi-layer optimizations, present variants as an incremental journey: "Our first attempt was X (Y% improvement). However... We thus propose Z (W% over X)."
- **Formalize the problem.** When decisions depend on I/O patterns, define notation first (`I/O = (offset, length)`), then enumerate cases with formal conditions.
- **Explicit scope.** State what you do NOT address: "This paper does not aim to redesign X since Y is already well-studied."

**Pitfalls:** Orphan design points. Describing WHAT without WHY. Figure never referenced. No trade-off acknowledged. No goals-to-techniques mapping.

---

## Implementation

- **Platform:** Language, LOC, OS/kernel version, hardware. Name the base system(s).
- **Key data structures only.** Layout, field sizes, why those sizes matter.
- **Engineering challenges.** What broke, how you fixed it. Builds credibility.
- **Don't repeat Design.** Implementation = *how*; Design = *what* and *why*.

---

## Evaluation (Systems-Specific)

### Structure

1. **Questions-driven opening.** 4-6 questions, each anchoring a subsection with `\ref{}`.
2. **Setup & Methodology** (before any results):
   - Testbed, competitors (explain missing baselines), workloads (table), methodology (threads, runs, stddev <5%).
   - **For crash consistency:** injection points, 1000+ random tests, result.
3. **Macro:** Headline + why wins + why loses. Red improvement % above bars.
4. **Micro:** Isolate each design point. Show *why*, not just *that*.
5. **Sensitivity:** Vary key parameters.
6. **Platform generalization (optional):** "Does the design generalize beyond current hardware?"

**Pitfalls:** Normalizing to self. No error bars. Graphs without WHY. Missing baseline configs. Silent about missing baselines. Hiding technique limitations.

---

## Related Work

- **Opening:** "To the best of our knowledge, [System] is the first to [unique contribution]."
- **Structure:** 3-4 thematic categories. Per category: what existing work does → how you differ.
- **Be fair.** Authors may review your paper. No paper dumps — group and compare.
- **Name the double-overhead problem** if your system integrates with existing layers.

---

## Discussion & Defense Patterns (System-Specific)

- **Be concrete.** "Currently evaluated up to N threads; beyond this, X dominates" — not "May not scale."
- **Distinguish design vs. implementation limits.**
- **"Shall we..." questions.** Frame alternatives, answer with data, explain the trade-off.
- **"Why do prior systems..." defense.** Explain historical context for design choices you're departing from.
- **"We do acknowledge..." concession.** When rejecting an alternative, acknowledge its merit.
- **"We fail to run X despite our best efforts."** — honesty about missing baselines builds credibility.
- **2-3 future directions.** Each names a specific approach + what makes it non-trivial.

## Conclusion

**5 sentences max:** problem → insight → what built → key result → closing. No new claims. No bullet points. No "Future work."

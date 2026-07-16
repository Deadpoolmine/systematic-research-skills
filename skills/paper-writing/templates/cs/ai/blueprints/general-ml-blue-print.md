# General ML Paper Blueprint

**Load this reference when:** writing an ML/AI paper targeting NeurIPS, ICML, ICLR, ACL, AAAI, or COLM. Provides page budget, per-section paragraph plans, and the narrative framework distilled from leading ML researchers (Nanda, Farquhar, Lipton, Steinhardt, Perez).

**Skeleton:** varies by venue — see `templates/ai/BLUEPRINT.md` for skeleton mapping.

---

## The Narrative Principle

> "A paper is a short, rigorous, evidence-based technical story with a takeaway readers care about." — Neel Nanda

**Three pillars** (must be clear by end of introduction):

| Pillar | Description |
|--------|------------|
| **The What** | 1-3 specific novel claims within a cohesive theme |
| **The Why** | Rigorous empirical evidence supporting claims |
| **The So What** | Why readers should care — connection to community problems |

**If you cannot state your contribution in one sentence, you don't yet have a paper.**

---

## Page Budget

**All page limits below are for MAIN CONTENT ONLY. References do NOT count toward the page limit at ANY venue listed.** Appendices are also unlimited (reviewers not required to read).

| Conference | Submission | Camera-Ready | Notes |
|-----------|-----------|--------------|-------|
| NeurIPS | 9 pages + refs | +0 | Mandatory checklist, lay summary |
| ICML | 8 pages + refs | +1 | Broader Impact Statement |
| ICLR | 9 pages + refs | +1 | LLM disclosure |
| ACL | 8 pages (long) + refs | varies | Limitations mandatory |
| AAAI | 7 pages + refs | +1 | Strict style adherence |
| COLM | 9 pages + refs | +1 | LM focus |

When allocating paragraph budget, only count the main-content pages — references are extra.

---

## Time Allocation (Neel Nanda)

Spend **equal time** on each:
1. The abstract
2. The introduction
3. The figures
4. Everything else combined

**Why?** Reviewers form judgments before reaching methods. Encounter order: title → abstract → introduction → figures → maybe the rest.

---

## Per-Section Plans

### Paragraph Budget (BINDING — 7-page paper, 2-column)

| Section | Paragraphs | % of Paper | Notes |
|---------|-----------|------------|-------|
| Abstract | 1 (5 sentences) | 3% | 5-sentence formula, no generic opening |
| Introduction | 7-8 | 18% | Ends with contribution bullets |
| Related Work | 5-6 | 13% | Thematic grouping, not paper-by-paper |
| Method | 12-14 | 30% | Architecture figure + 2-3 subsections |
| Experiments | 10-12 | 26% | Setup, main results, ablations, analysis |
| Discussion and Limitations | 3-4 | 7% | Specific limitations, failure modes, future work |
| Conclusion | 1-2 | 3% | 3-5 sentence summary, no new information |

Scale proportionally for 8-9 page venues. Never exceed 3-5 sentences per paragraph. Maximum 6 sentences.

### Abstract (5-Sentence Formula — Sebastian Farquhar)

1. **What you achieved:** "We introduce/prove/demonstrate..."
2. **Why this is hard and important**
3. **How you do it** (with specialist keywords for discoverability)
4. **What evidence you have**
5. **Your most remarkable number/result**

Delete generic openings like "Large language models have achieved remarkable success..."

### Introduction (1-1.5 pages max)

Must include:
- Clear problem statement with evidence
- Brief approach overview
- **Contributions (bullet list, END of Introduction):** 2-3 bullets max. One line each. Pattern:
  1. **Identify** problem
  2. **Propose** insight/technique (merge if possible)
  3. **Demonstrate** results
- Paper Organization paragraph (1-2 sentences, optional — omit if space tight)
- Methods should start by page 2-3

### Figure 1 (Draft Before Writing)

Figure 1 deserves special attention — many readers skip directly to it:
- Convey core idea, approach, or most compelling result
- Vector graphics (PDF/EPS)
- Self-contained caption
- Colorblind-safe palette (Okabe-Ito or Paul Tol)
- Verify grayscale readability (8% of men have color vision deficiency)

### Methods

Enable reimplementation:
- Conceptual outline or pseudocode
- All hyperparameters listed
- Architectural details sufficient for reproduction
- Present final design decisions; ablations go in experiments

### Experiments

For each experiment, explicitly state:
- What claim it supports
- How it connects to main contribution
- Experimental setting (details in appendix)
- What to observe: "the blue line shows X, which demonstrates Y"

Requirements:
- Error bars with methodology (std dev vs std error)
- Hyperparameter search ranges
- Compute infrastructure (GPU type, total hours)
- Seed-setting methods

### Related Work

Organize by methodology, not paper-by-paper:
- ✅ "One line of work uses assumption X [refs]; we use assumption Y because..."
- ❌ "Smith et al. introduced X while Jones et al. introduced Y."

Cite generously — reviewers likely authored relevant papers.

### Discussion and Limitations (REQUIRED)

**Discussion:**
- Honest reflection on what worked and what didn't
- Broader implications of the results

**Limitations:**
- Be specific. "Requires 8×A100 GPUs for training" not "computationally expensive"
- Failure modes: when doesn't it work? Show a concrete example.
- Reviewers instructed not to penalize honest limitation acknowledgment
- Pre-empt criticisms by identifying weaknesses first
- Explain why limitations don't undermine core claims

**Future work:** 2-3 concrete directions that naturally extend this work. Not a different paper.

### Conclusion

**Purpose:** Remind the reader what they learned. No new information.

**Structure:**
1. Task and gap (1 sentence)
2. Key insight (1 sentence)
3. What you proposed (1 sentence)
4. Key result (1 sentence)
5. Closing remark (1 sentence — optional)

**Pitfalls:** Introducing new claims, repeating the abstract, "Future work includes..." (belongs in Discussion).

---

## Writing Style Guidelines

### Sentence-Level (Gopen & Swan)

| Principle | Rule |
|-----------|------|
| Subject-verb proximity | Keep subject and verb close |
| Stress position | Emphasis at sentence ends |
| Topic position | Context first, new info after |
| Old before new | Familiar → unfamiliar |
| One unit, one function | Each paragraph = one point |
| Action in verb | Use verbs, not nominalizations |

### Micro-Level (Ethan Perez)

- Minimize pronouns: ❌ "This shows..." → ✅ "This result shows..."
- Verbs early: position verbs near sentence start
- Delete filler: "actually," "a bit," "very," "really," "basically"

### Word Choice (Zachary Lipton)

- Be specific: ❌ "performance" → ✅ "accuracy" or "latency"
- Eliminate hedging: drop "may" and "can" unless genuinely uncertain
- Delete intensifiers: ❌ "provides *very* tight approximation" → ✅ "provides tight approximation"

### Precision (Jacob Steinhardt)

- Consistent terminology — pick one term per concept and stick with it
- State assumptions formally before theorems
- Intuition + rigor: intuitive explanations alongside formal proofs

---

## What Reviewers Actually Read

| Section | % Who Read | Implication |
|---------|-----------|-------------|
| Abstract | 100% | Must be perfect |
| Introduction | 90%+ (skimmed) | Front-load contribution |
| Figures | Examined before methods | Figure 1 is critical |
| Methods | Only if interested | Don't bury the lede |
| Appendix | Rarely | Supplementary only |

---

## Quality Checklist

- [ ] One-sentence contribution is clear
- [ ] Abstract follows 5-sentence formula
- [ ] Introduction ≤ 1.5 pages, methods start by page 2-3
- [ ] Figure 1 is compelling and self-contained
- [ ] Every experiment states what claim it supports
- [ ] Error bars with methodology stated
- [ ] Limitations section present and specific
- [ ] Conclusion separate from Discussion, no new claims
- [ ] Related work grouped by methodology
- [ ] All citations verified (no hallucinated references)

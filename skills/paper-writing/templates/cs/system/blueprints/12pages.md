# 12-Page Systems Paper Blueprint

**Load this reference when:** writing a 12-page systems paper targeting OSDI, SOSP, FAST, NSDI, ATC, EuroSys, or ASPLOS. Provides page budget, per-section paragraph plans, and venue conventions distilled from authoritative systems writing guides.

**Skeleton:** USENIX venues → `templates/cs/system/usenix/` | ACM venues → `templates/cs/system/acm/`

---

## Page Budget

| Section | Pages | Key Constraint |
|---------|-------|---------------|
| Abstract | ~0.25 | 150-250 words, 5 sentences |
| S1 Introduction | 1.5-2 | Must state thesis: "X is better for Y in Z" |
| S2 Background & Motivation | 1-1.5 | Define-before-use; include production observations |
| S3 Design | 3-4 | Every design choice discusses alternatives |
| S4 Implementation | 0.5-1 | Prototype details, LOC, key engineering decisions |
| S5 Evaluation | 3-4 | Every conclusion stated 3× (hypothesis, result, caption) |
| S6 Related Work | 1 | Grouped by methodology, not paper-by-paper |
| S7 Conclusion | 0.5 | 3-sentence formula |
| **Total** | **~12** | References unlimited |

---

## Per-Section Paragraph Plans

### Abstract (5 sentences)

1. Problem context and importance
2. Gap in existing approaches
3. Key insight / thesis
4. Summary of approach and key results
5. Broader impact or availability

### S1 Introduction

1. **Problem statement** (~0.5p) — Domain context with concrete numbers (cluster sizes, workload stats, latency requirements)
2. **Gap analysis** (~0.5p) — Enumerate gaps G1-Gn in existing systems. Each gap: one sentence + evidence.
3. **Key insight** (1 paragraph) — Thesis: "X is better for applications Y running in environment Z"
4. **Contributions** (~0.5p) — Numbered list of 3-5 testable contributions. Each maps to a paper section.

### S2 Background & Motivation

1. **Technical background** (~0.5p) — Define terms and systems the reader needs. Follow define-before-use.
2. **Production observations** (~0.5-1p) — Present Observation 1, 2, 3 from real data or measurements. Each observation leads to a design insight.

### S3 Design

1. **Architecture overview** (~0.5p) — Figure first, then walkthrough of components and data flow
2. **Module-by-module** (~2-2.5p) — Per subsection: what the module does → design choice → alternatives considered → why this choice
3. **Design alternatives** (~0.5-1p) — For each major decision, explicitly discuss what was NOT chosen and why

### S4 Implementation

1. **Prototype** — Language, framework, LOC, integration points
2. **Key engineering** — Non-obvious implementation choices worth documenting

### S5 Evaluation

1. **Setup** (~0.5p) — Hardware, baselines, workloads, metrics. Reproducible.
2. **End-to-end** (~1-1.5p) — X vs baselines for application Y on environment Z
3. **Microbenchmarks / Ablation** (~1-1.5p) — Isolate each design decision's contribution
4. **Scalability** (~0.5p) — Behavior as problem size or load increases

**Critical rule:** State every experimental conclusion 3 times:
- Section opening: hypothesis ("We expect X to outperform Y because...")
- Section closing: conclusion ("Results show X outperforms Y by Z%")
- Figure caption: evidence ("Figure N shows X achieves Z% better throughput than Y")

### S6 Related Work

- Group by methodology or approach (not paper-by-paper)
- Per group: what they do → limitation → how your work differs
- Use comparison table when comparing 4+ systems

### S7 Conclusion

Three sentences:
1. The hypothesis / problem addressed
2. The solution approach
3. The key result

---

## Writing Patterns

| Pattern | Description | When to Use |
|---------|------------|------------|
| **Gap Analysis** | Enumerate gaps G1-Gn in Introduction → map to answers A1-An in Design | When your contribution fills specific, nameable gaps |
| **Observation-Driven** | Present production observations (O1-O3) → derive insights → build system | When you have real workload/production data |
| **Contribution List** | Numbered contributions in Intro, each mapping to a section | When contributions are cleanly separable |
| **Thesis Formula** | Structure entire paper around "X is better for Y in Z" | Always — this is the backbone |

---

## Quality Checklist

- [ ] Thesis follows "X is better for Y in Z"
- [ ] Introduction has numbered contributions (3-5), each maps to a section
- [ ] Design discusses alternatives for every major choice
- [ ] Every evaluation conclusion stated 3× (hypothesis, result, caption)
- [ ] Related work grouped by methodology
- [ ] Page budget within limits
- [ ] All design points trace to L0 key idea

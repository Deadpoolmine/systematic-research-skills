# System Paper Writing Guide

**Load this reference when:** writing or polishing a system paper. Provides conventions, voice guidance, and common pitfalls for CS systems venues (OSDI, SOSP, EuroSys, ASPLOS, ATC, FAST, NSDI, etc.).

**Relationship to L1:** The sections below describe **typical writing conventions** for common section types. The actual section structure is determined in L1 through discussion with the user — not copied from this guide. If L1 produces a section not listed here, apply the overall voice principles and adapt from the closest matching section.

---

## Overall Voice

Act as an academic editor refining for top CS systems venues (FAST, ASPLOS, ATC, OSDI, SOSP, SIGMOD, NSDI, EuroSys).

- **Confident but measured.** State what you did and what happened. Avoid marketing language ("revolutionary", "game-changing").
- **Precise.** Numbers have units. Claims have evidence. Comparisons name the baseline and the metric.
- **Honest.** Acknowledge limitations. A paper that admits weaknesses is more credible than one that pretends perfection.
- **First person plural** ("we") is standard. Avoid passive voice where it obscures the actor.
- **Minimal intervention.** If the content is already clear and correct, don't change words or expressions just to make them different. Fix what's broken; leave what works.
- **Preserve LaTeX.** Never break `\ref{}`, `\cite{}`, `\includegraphics{}`, math mode, or any LaTeX syntax during editing.

| ✅ Good | ❌ Bad |
|---------|--------|
| "We measure 2.3× higher throughput than Ext4 on the Varmail workload." | "Our system dramatically outperforms existing solutions." |
| "The design does not address network-attached storage; we leave this to future work." | (no limitations mentioned) |
| "Figure 3 shows that latency drops by 40% when enabling feature X." | "Feature X improves latency." |

---

## Introduction

### Purpose
Convince the reader this paper is worth their time. Establish territory → identify gap → present your solution → preview results.

### Structure & Advice

**Big Background (1 paragraph):** Name the trend. Be specific — "CXL-attached memory" not "new hardware". Cite 2-3 key references that establish the importance of this trend.

**Small Background (1 paragraph):** Narrow to your domain. What subsystem or problem space? Who cares and why? The reader should think "yes, this matters."

**Challenge (1 paragraph):** The most important paragraph in the paper. Three elements:
1. **What** is the problem? State it in one sentence.
2. **Evidence** — cite data. "Motivation measurements show 38% overhead" beats "this is a problem."
3. **Why** haven't existing solutions solved it? One sentence on the root cause.

**Key Idea (1 paragraph):** ONE insight. Not "we built a system" but "our insight is that X can be merged with Y, eliminating Z." The insight should feel surprising yet obvious in retrospect.

**Design Preview (1 paragraph):** Name your 2-3 design points. Each gets 1-2 sentences. Show how each serves the key idea.

**Experiment Summary (2-3 sentences):** Tease the headline numbers. "Outperforms state-of-the-art by 30% on production traces" is more compelling than a list of benchmarks.

**Contributions (bullet list):** 3-4 bullets. Each starts with a verb or concrete noun. Not "We studied X" but "A measurement study of X revealing Y."

### Pitfalls
- Starting with a generic sentence ("In recent years, data volumes have grown exponentially...") — start with YOUR domain
- The "laundry list" contributions ("We designed, implemented, evaluated, and open-sourced...") — these are table stakes
- Hiding the key insight behind system description

---

## Background & Motivation

### Purpose
Build the reader's mental model. By the end, they should feel the pain that motivates your solution.

### Structure & Advice

**Background concepts:** Don't teach a textbook. Explain only what's needed to understand YOUR contribution. If a concept is well-known in your community, cite it and move on.

**Motivation measurements (if applicable):** This is where you show data that proves the problem exists. A good motivation section:
- Measures on real hardware with real workloads
- Compares reasonable baselines (not strawmen)
- Explains WHY the numbers are what they are
- Leads inexorably to "therefore we need a new approach"

**Gap analysis:** What do existing solutions do? Where do they fall short? Be fair to prior work — you'll cite these papers as related work, and their authors will review your paper.

### Pitfalls
- Teaching fundamentals the reader already knows
- Motivation numbers that don't actually motivate ("10% overhead" is not "70% overhead")
- Unfair baseline comparisons in motivation (save fair comparisons for Evaluation)

---

## Design

### Purpose
This is the intellectual contribution. The reader should understand WHAT you built, WHY those choices, and HOW they realize the key idea.

### Structure & Advice

**Design goals:** Derive 3-4 non-negotiable requirements from the challenge. Each goal should be testable. "Low overhead" is not a goal; "< 5% CPU overhead on saturated workloads" is.

**System overview:** One architecture diagram. Walk through the components and their relationships. The reader should understand the big picture before diving into details.

**Design points (2-3):** Each design point gets its own subsection. For each:
1. **What** — the mechanism or technique
2. **Why** — why this design over alternatives (name the alternatives)
3. **How** — how it serves the key idea (explicitly connect to L0 point #4)
4. **Trade-off** — what does this design give up? Every design has a cost; acknowledging it builds credibility

**Algorithms/pseudocode:** Use when the mechanism is non-obvious. Describe in prose first, then show pseudocode. The prose explains WHY; the pseudocode shows HOW.

### Pitfalls
- Design points that don't trace to the key idea (orphan contributions)
- Describing WHAT without explaining WHY
- Architecture diagram that's never walked through in the text
- No discussion of alternatives considered

---

## Implementation

### Purpose
Prove you built a real system. This section is about engineering — what did it take to make the design work?

### Structure & Advice

**Platform details:** Language, LOC, OS version, hardware. These establish credibility. "Implemented as a Linux kernel module (12K LOC)" tells the reader this is real.

**Key data structures and algorithms:** The implementation details that matter for correctness or performance. Don't list every struct field — highlight the critical ones.

**Engineering challenges:** What problems arose during implementation that the clean design didn't anticipate? How did you solve them? This section humanizes the paper and provides useful information for practitioners.

### Pitfalls
- Listing every implementation detail ("we used a hash table with 1024 buckets") — focus on what matters
- No engineering challenges mentioned (makes the paper seem unreal)
- Repeating design section content in implementation language

---

## Evaluation

### Purpose
Answer: does the system work? By how much? Under what conditions? What are the limits?

### Structure & Advice

**Experimental setup:** Be thorough. Another researcher should be able to reproduce. Include:
- Hardware specs (CPU model, memory, storage devices)
- Software versions (kernel, libraries, compiler flags)
- Workload descriptions (why these workloads?)
- Baseline descriptions and configurations
- Methodology (warm-up, runs, error bars, cold/hot cache state)

**Macro-benchmarks:** End-to-end results. Start with the headline figure. Then explain:
- WHY does your system win? (not just THAT it wins)
- WHY does it lose where it loses? (be honest)
- Connect results to design points — "The 2× improvement on workload X comes from design point 1, which..."

**Micro-benchmarks:** Isolate each design point's contribution. Show that each matters. If one design point contributes 2% and another 50%, that's worth knowing.

**Sensitivity analysis:** How does performance vary with key parameters? Shows robustness.

**Draft mode:** If experiments are incomplete, use `[TODO: actual number]` placeholders. The setup, baselines, and methodology must be fully specified — only numbers can be placeholders. Expected trends should be stated ("We expect design point 1 to improve throughput by 2-3×").

### Pitfalls
- Normalizing to your own system (always show absolute numbers somewhere)
- Cherry-picking favorable results
- No error bars or variance information
- Graphs without explanation of WHY
- Missing baseline configurations (unfair comparison)

---

## Related Work

### Purpose
Position your work. Show you understand the literature. Be fair.

### Structure & Advice

**Thematic organization:** Group by theme, not chronologically. 3-4 categories. Each category:
1. What has been done (cite key works)
2. How your work differs (not "they're worse" but "they target X while we target Y")
3. Be generous where honest — the authors of these papers may review yours

### Pitfalls
- The "data dump" — listing papers without connecting to your work
- Unfairly dismissing prior work to make yours look better
- Missing important related work (reviewers will notice)

---

## Discussion / Limitations

### Purpose
Show intellectual honesty. Every paper has limits — acknowledging them builds trust.

### Advice
- Be specific about limitations ("Does not support distributed deployments" not "May not work at scale")
- Distinguish between limitations of the IMPLEMENTATION vs the DESIGN
- Suggest future work that naturally extends your contribution

---

## Conclusion

### Purpose
Remind the reader what they just learned. No new information.

### Structure
1. Problem (1 sentence)
2. Key insight (1 sentence)
3. What you built (1 sentence)
4. Key result (1 sentence)
5. Closing statement (1 sentence — optional, can be forward-looking)

### Pitfalls
- Introducing new claims not in the body
- Repeating the abstract verbatim
- Generic closing ("We believe this work opens exciting avenues for future research")

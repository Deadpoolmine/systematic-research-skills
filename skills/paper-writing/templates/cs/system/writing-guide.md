# System Paper Writing Guide

**Load when:** writing/polishing systems papers (OSDI, SOSP, EuroSys, ASPLOS, ATC, FAST, NSDI, SIGMOD).

---

## Overall Voice

- **Confident, measured.** State what you did. No marketing ("revolutionary", "game-changing").
- **Precise.** Numbers have units. Claims name baseline + metric.
- **Honest.** Acknowledge limitations. Credibility > perfection.
- **"we"**. First person. Avoid passive where it obscures actor.
- **Minimal intervention.** Fix what's broken; leave what works.
- **Paragraph structure.** Topic → 2-3 support → conclude/transition (总分总). One idea = one chain step.
- **Paragraph length.** 3-5 sentences. Hard cap: 6. Sentence hard cap: 30 words.
- **Vocabulary.** Plain English. No: ameliorate, delineate, elucidate, heretofore, utilize, leverage.
- **Blueprint is binding.** Section structure + paragraph count + page budget are HARD constraints.
- **Preserve LaTeX.** Never break `\ref{}`, `\cite{}`, `\includegraphics{}`, math mode.

| ✅ | ❌ |
|----|----|
| "2.3× higher throughput than Ext4 on Varmail." | "Dramatically outperforms existing solutions." |
| "Does not address network-attached storage." | No limitations. |
| "Figure 3: latency drops 40% with feature X." | "Feature X improves latency." |

---

## Introduction (1-1.5pg max)

| Step | Rule |
|------|------|
| Big Background | Name trend. Specific: "CXL-attached memory" not "new hardware". Cite 2-3. |
| Small Background | Narrow to domain. Who cares, why. |
| Challenge | Problem (1 sent) + evidence (data, not hand-waving) + root cause. |
| Key Idea | ONE insight. Not "we built X" but "X merges with Y, eliminating Z." |
| Design Preview | 2-3 design points, 1-2 sent each. Tie to key idea. |

**Contributions (END of Intro):** 2-3 bullets, 1 line each. Pattern: (1) Identify problem → (2) Propose insight/technique → (3) Demonstrate results. Optional: Paper Organization after.

**Pitfalls:** Generic opening. Laundry-list contributions. Hiding insight behind system description.

## Background & Motivation

Background: only what's needed. Motivation: real hardware, real workloads, fair baselines. Lead inexorably to "we need a new approach." No textbook teaching.

## Design

Design goals: 3-4 testable requirements ("<5% CPU overhead" not "low overhead"). Architecture figure (required). Per design point: what → why (name alternatives) → how it serves key idea → trade-off acknowledged.

**Pitfalls:** Orphan design points. Describing WHAT without WHY. Figure never walked through.

## Implementation

Platform: language, LOC, OS, hardware. Key structures only. Engineering challenges: what broke, how you fixed it. Don't repeat Design.

## Evaluation

**Setup:** hardware, software, workloads (why?), baselines (how tuned?), methodology (warm-up, runs, error bars, cache state). **Macro:** headline + why wins + why loses. **Micro:** isolate each design point. **Sensitivity:** vary key params. **Draft:** `[TODO: number]`. Setup/methodology fully specified.

**Pitfalls:** Normalizing to self. No error bars. Graphs without WHY. Missing baseline configs.

## Related Work

Group by theme (3-4 categories). Per category: what's done → how you differ. Be fair — authors review your paper. No paper dumps.

## Discussion / Limitations

Specific: "No distributed support" not "May not scale." Distinguish implementation vs design limits. 2-3 concrete future directions.

## Conclusion

5 sentences: problem → insight → what built → key result → closing. No new claims. No "Future work" (→ Discussion).

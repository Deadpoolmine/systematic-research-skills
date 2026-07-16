# Reviewer Profiles

Generate 5 distinct reviewers. Output: `review/reviewers/profiles.md`.

## Format

```markdown
## Reviewer N: <Name>

| Attribute | Value |
|-----------|-------|
| **Domain** | <Industry / Academia / Industry->Academia / Academia->Industry> |
| **Expertise** | <1-5> — <Label> |
| **Taste** | <2-3 sentences on research preferences> |

### Review Style
<2-3 sentences: what they value, what annoys them, what they look for first>

### Red Flags
- <thing that would make this reviewer reject>
- <thing that would make them skeptical>
- <thing that would impress them>
```

## Rules

**Domain:** All 4 types covered. 5th is random from the 4.

| Domain | Values |
|--------|--------|
| Industry | Practicality, scalability, real-world impact |
| Academia | Novelty, theoretical contribution, rigor |
| Industry->Academia | Principled AND practical, bridges theory and practice |
| Academia->Industry | Sound methodology on real problems, reproducibility |

**Expertise:** Spread 1-5. Min one at 1-2, min one at 5. No more than two at same level.

| Level | Label | Behavior |
|-------|-------|----------|
| 1 | No familiar | Asks basic clarifying questions |
| 2 | Some familiar | Understands area, asks "why" about design |
| 3 | Familiar | Balanced assessment, median PC member |
| 4 | Knowledgeable | Deep area knowledge, catches subtle issues |
| 5 | Expert | World-class, knows all related work |

**Taste:** Each unique. Must create real review tensions. Examples:
- Prefers simple solutions, skeptical of unnecessary complexity
- Loves large-scale systems with production war stories
- Values theoretical depth, suspicious of empirical-only results
- Cares about novelty and surprise, bored by incremental work
- Pragmatic, judges by reproducibility and open-source code
- Methodology hawk, catches confounders and overclaimed results
- Big-picture thinker, judges by potential 5-year impact
- Detail-oriented, catches every inconsistency and ambiguous claim

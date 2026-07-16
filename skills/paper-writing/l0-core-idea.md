# L0 — Core Idea Stream

**Load when:** executing L0 of paper-writing.

## Checklist

1. **Determine venue** — ask first. Dictates page budget -> blueprint -> skeleton.
2. **Discover blueprint** — list `templates/`, load `BLUEPRINT.md` matching venue field + page count.
3. **Judge core points** — one question at a time. PASS / WEAK / REJECT per answer. Loop until all PASS.

## Core Points

Minimum: points 1-3 + (Key Idea OR Design Points). Key Idea recommended but skip if challenge-driven (3 challenges -> 3 designs, no single insight).

| # | Point | Req | Question | Reject If |
|---|-------|-----|----------|-----------|
| 1 | **Big Background** | Yes | Macro trend / tech shift? | Vague, no academic relevance |
| 2 | **Small Background** | Yes | Specific domain? | Not concrete, no link to big |
| 3 | **Existing Challenges** | Yes | Problem + data + severity? | No data, trivial, unsubstantiated |
| 4 | **Key Idea** | Rec | ONE insight that solves it? | Doesn't address challenge |
| 5 | **Design Points (2-3)** | Yes* | Contributions? | <2 or >3, don't address challenges |
| 6 | **System & Experiments** | Yes | Built? Experimental plan? | No system AND no plan |

> *Required if no Key Idea. Experiments: plan accepted (prototype + benchmarks + baselines + expected ranges OK).

## Output

`docs/systematic-research/plans/YYYY-MM-DD-<topic>-stream-L0.md`:

```markdown
# L0: <Topic> | Venue: <venue> | YYYY-MM-DD

## 1. Big Background
## 2. Small Background
## 3. Existing Challenges
## 4. Key Idea *(skip if challenge-driven)*
## 5. Design Points
- DP1: <desc> -> addresses <challenge> by <mechanism>
- DP2/DP3: ...
## 6. System & Experiments
**System:** <status> | **Benchmarks:** <plan> | **Expected:** <ranges OK>
```

Commit: `L0: core idea for <topic>`. Proceed to L1.

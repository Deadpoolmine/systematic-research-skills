# L1 — Chapter Structure Stream (The Architect Phase)

**Load when:** executing L1. Defines the discussion-driven process for custom Section/Subsection structures.

**REQUIRED BACKGROUND:** paper-writing SKILL.md hard gates. L0 must be complete with venue.

## Checklist

1. **Re-read L0.** Venue known. Answer: primary contribution? What must reader understand first? What evidence needed?
2. **Discover blueprint.** Explore `templates/` → find field category → load `BLUEPRINT.md` → match blueprint by page count. Blueprint provides page budget — constrain scope.
3. **Propose 2-3 custom structures.** NOT from a template. Derived from THIS paper's story. Present trade-offs. Recommend one.
4. **Define A→B→C flow chains** — one Section at a time, in discussion. Propose each chain, user confirms/rejects.
5. **Propose figure placeholders** — at natural flow chain steps: `[Figure: <description>. File: figs/<name>.pdf]`. User confirms each.
6. **Write L1 document.** Every Section name, Subsection name, chain item = product of discussion.

## Flow Chain Rules

Each chain item is a **logical step** — what the reader must understand before the next. One idea per step. Ordered by dependency. Descriptive ("Why existing solutions fail"), not numbered ("Step 3").

## Figure Placeholders

| Type | When | Typical Placement |
|------|------|------------------|
| Architecture/Pipeline overview | Design/Method — reader needs big picture first | Before component descriptions |
| Motivation graph | Background — data proving the problem | Within challenge/gap step |
| Main result graph/table | Evaluation — headline comparison | Macro-benchmarks |
| Ablation/breakdown | Evaluation — isolate contributions | Micro-benchmarks |
| Qualitative example | Analysis — what output looks like | After quantitative results |

## Output

```markdown
# L1 Chapter Structure Stream: <Topic> | Venue: <venue> | Date: YYYY-MM-DD

## Section 1: <Name from discussion>
A. <step> → B. <step> → C. <step> → ...

## Section 2: <Name from discussion>
### Subsection 2.1: <Name>
A. <step> → B. <step> → C. <step>
```

Commit with `L1: structure for <topic>`. Proceed to L2.

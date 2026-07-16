# L1 — Chapter Structure Stream (The Architect Phase)

**Load when:** executing L1. Defines the discussion-driven process for custom Section/Subsection structures.

**REQUIRED BACKGROUND:** SKILL.md hard gates. L0 complete with venue.

## Mode: Write vs Polish

| Mode | Starting Point | Action |
|------|---------------|--------|
| **Write** | L0 only (no draft) | Propose 2-3 custom structures. Define chains from scratch. |
| **Polish** | L0 + existing draft | Read draft → extract implicit structure → present: "Here's the structure I see. Does this match your intent? What Sections need reordering, splitting, or merging?" → discuss → revise |
| **Polish (L1 exists)** | Existing `stream-L1.md` | Critical review: flow chains still accurate? Figures in right places? → discuss changes |

## Checklist

1. **Re-read L0.** Venue known.
2. **Discover blueprint.** Explore `templates/` → load `BLUEPRINT.md` → match by page count. Page budget constrains scope.
3. **Propose structure.** Write: 2-3 custom options. Polish: extract from draft + propose modifications. Present trade-offs. User confirms.
4. **Define A→B→C flow chains** — one Section at a time, in discussion. Write: build chains. Polish: review existing chains, revise.
5. **Propose figure placeholders** — `[Figure: <description>. File: figs/<name>.pdf]`. Polish: check existing figures against flow chains.
6. **Write L1 document.** Every Section/Subsection/chain = product of discussion.

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

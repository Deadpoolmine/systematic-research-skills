# L1 — Chapter Structure Stream (The Architect Phase)

**Load when:** executing L1. Defines the discussion-driven process for custom Section/Subsection structures.

**REQUIRED BACKGROUND:** SKILL.md hard gates. L0 complete with venue.

<HARD-GATE-L1-STEPWISE>
**ONE Section at a time.** Propose → discuss → user confirms → define chain → NEXT Section.
Do NOT present all Sections at once.
Do NOT ask user to confirm the entire structure in one go.
Each Section must be confirmed (name + flow chain) before moving to the next.
</HARD-GATE-L1-STEPWISE>

## Mode: Write vs Polish

| Mode | Starting Point | Action |
|------|---------------|--------|
| **Write** | L0 only (no draft) | Propose Sections ONE AT A TIME. For each: propose name → discuss → define A→B→C chain → user confirms → next. |
| **Polish** | L0 + existing draft | Extract implicit structure → **critical think** (identify 2-3 issues + suggestions) → present issues ONE AT A TIME → discuss each → **write `stream-L1.md`** |
| **Polish (L1 exists)** | Existing `stream-L1.md` | Critical review → **critical think** (2-3 issues + suggestions) → present issues ONE AT A TIME → discuss each → update |

## Critical Think (Polish Mode)

Before presenting to the user, silently review:

1. **Structural flow** — do Sections build on each other logically? Are there gaps or redundancies?
2. **Chain fidelity** — does the draft actually follow the extracted A→B→C flow, or does it wander?
3. **Page budget fit** — does each Section's depth match its page allocation from the blueprint?
4. **Figure placement** — are figures at natural breakpoints in the flow? Any missing visual anchors?

Present issues **ONE AT A TIME**. For each: "Issue: [X]. Suggestion: [Y]. Agree?" Wait for user before next issue.

## Checklist

1. **Re-read L0.** Venue known.
2. **Discover blueprint.** Explore `templates/` → load `BLUEPRINT.md` → match by page count. Page budget constrains scope.
3. **Propose Section 1** — name, purpose, how it maps to L0. User confirms. Then define its A→B→C chain. User confirms chain.
4. **Propose Section 2** — same process. Then Section 3, Section 4... ONE AT A TIME.
5. **Propose figure placeholders** — after each Section's chain is confirmed: "Here's where figures go in this Section: [list]. OK?"
6. **Write L1 document.** Accumulate incrementally — append each confirmed Section to `stream-L1.md` as you go.

## Step-by-Step Interaction Protocol

```dot
digraph l1_flow {
    rankdir=TB;
    "Re-read L0" [shape=box];
    "Discover blueprint" [shape=box];
    "Propose Section 1 name" [shape=box];
    "User confirms name?" [shape=diamond];
    "Define Section 1 chain" [shape=box];
    "User confirms chain?" [shape=diamond];
    "Propose figures for S1" [shape=box];
    "Propose Section 2 name" [shape=box];
    "User confirms name?" [shape=diamond];
    "Define Section 2 chain" [shape=box];
    "User confirms chain?" [shape=diamond];
    "Propose figures for S2" [shape=box];
    "...Section N" [shape=box];
    "Write L1 doc + commit" [shape=oval];

    "Re-read L0" -> "Discover blueprint";
    "Discover blueprint" -> "Propose Section 1 name";
    "Propose Section 1 name" -> "User confirms name?";
    "User confirms name?" -> "Propose Section 1 name" [label="no"];
    "User confirms name?" -> "Define Section 1 chain" [label="yes"];
    "Define Section 1 chain" -> "User confirms chain?";
    "User confirms chain?" -> "Define Section 1 chain" [label="no"];
    "User confirms chain?" -> "Propose figures for S1" [label="yes"];
    "Propose figures for S1" -> "Propose Section 2 name";
    "Propose Section 2 name" -> "User confirms name?";
    "User confirms name?" -> "Propose Section 2 name" [label="no"];
    "User confirms name?" -> "Define Section 2 chain" [label="yes"];
    "Define Section 2 chain" -> "User confirms chain?";
    "User confirms chain?" -> "Define Section 2 chain" [label="no"];
    "User confirms chain?" -> "Propose figures for S2" [label="yes"];
    "Propose figures for S2" -> "...Section N";
    "...Section N" -> "Write L1 doc + commit";
}
```

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

## Per-Section Interaction Template

For EACH Section, follow this exact sequence:

1. **Propose name + purpose** — "Section N: `<name>`. Purpose: `<1 sentence>`. Maps to L0 point `<#N>`. OK?"
2. **Wait for user.** If rejected, revise. If accepted, proceed.
3. **Define flow chain** — "Chain: A. `<step>` → B. `<step>` → C. `<step>`. OK?"
4. **Wait for user.** If rejected, revise chain. If accepted, proceed.
5. **Propose figures** — "Figures in this Section: `[Figure: <desc>. figs/<name>.pdf]`. OK?"
6. **Append to L1 document.** Then move to next Section.

## Output

`docs/systematic-research/plans/YYYY-MM-DD-<topic>-stream-L1.md` — built incrementally, one Section at a time:

```markdown
# L1 Chapter Structure Stream: <Topic> | Venue: <venue> | Date: YYYY-MM-DD

## Section 1: <Name from discussion>
A. <step> → B. <step> → C. <step> → ...

## Section 2: <Name from discussion>
### Subsection 2.1: <Name>
A. <step> → B. <step> → C. <step>
```

Commit with `L1: structure for <topic>`. Proceed to L2.

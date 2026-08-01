# Routing and Invalidation Reference

## Entry-Point Decision

1. Inspect existing artifacts before interviewing the user.
2. If the core idea is absent, unstable, or contradicted by the draft, use `paper-writing` L0.
3. If L0 is current but section logic is absent or invalid, use L1.
4. If L0 and L1 are current but content is incomplete, use L2.
5. If content is complete, run L3 before independent review unless the user only requested a preliminary critique.
6. Use `paper-review` for independent criticism, not as a substitute for L3 consistency.
7. Route each review finding back to its earliest owning layer.

## Ambiguous Cases

| Situation | Route |
|---|---|
| Only a vague interest | L0; do not invent a thesis |
| Notes but no paper type | L0; keep type `undetermined` |
| Draft with no planning artifacts | Extract and critically review L0/L1 |
| Strong structure, weak prose | L2 then L3 |
| Language-only request | Polish-lite; do not restructure |
| Reviewer says “contribution unclear” | Inspect L0 before editing Introduction |
| Reviewer says “Section 3 is hard to follow” | Inspect L1 chain, then L2 prose |
| No experiments | Continue with support appropriate to paper type |
| New evidence contradicts a claim | L0 if core claim; otherwise owning L1/L2 scope |

## Invalidation Procedure

When an upstream artifact changes:

1. record the decision and reason;
2. identify direct dependents;
3. mark them `stale`;
4. revise the earliest affected artifact;
5. revalidate downstream artifacts in dependency order;
6. retire review findings that no longer apply, preserving their history.

Do not delete work merely because it is stale. Reuse unaffected material after validation.

## Safe Parallelism

Parallel-safe:

- independent source searches;
- independent read-only reviews;
- analysis of disjoint materials;
- figure work whose meaning is already frozen;
- disjoint sections after L1 contracts are accepted.

Serialize:

- edits to the same section;
- changes to L0 or L1;
- revisions where one output defines another task's input;
- final integration and consistency audit.

---
name: paper-orchestrator
description: Use when coordinating an academic paper across ideas, notes, drafts, figures, reviews, and revisions, especially when the correct next step or specialist paper skill is unclear.
---

# Paper Orchestrator

**Core principle:** Inspect the current paper project, route the next step to the right specialist, and recheck downstream work when an upstream decision changes.

<HARD-GATE>
Do NOT duplicate plans produced by `paper-writing` L0 Core Idea or L1 Chapter Structure. Before invoking a specialist, write a project checkpoint; after it finishes, update the same checkpoint. Do NOT let multiple workers edit the same Section. Do NOT declare completion while a blocking issue remains.
</HARD-GATE>

## Process Flow

```
Inspect project
    ↓
Choose earliest unresolved step
    ↓
Write checkpoint
    ↓
Run specialist skill
    ↓
Update checkpoint with result
    ↓
Output accepted?
    ├── no → Run specialist skill
    └── yes → Upstream changed?
                  ├── yes → Recheck affected work → Choose earliest unresolved step
                  └── no → Ready to deliver?
                              ├── no → Choose earliest unresolved step
                              └── yes → Done
```

## Step 1: Inspect

Inspect available notes, plans, drafts, figures, and reviews before asking questions. Identify the user's goal, current blocker, and existing artifacts from `paper-writing` L0 Core Idea or L1 Chapter Structure.

## Step 2: Route

| Current need | Route |
|---|---|
| Core idea, thesis, scope, venue, or contribution | `paper-writing` → L0 Core Idea |
| Section architecture or argument flow | `paper-writing` → L1 Chapter Structure |
| Drafting or revising Sections | `paper-writing` → L2 Section Writing |
| Cross-paper consistency or prose audit | `paper-writing` → L3 Consistency Audit |
| Figure design or production | `paper-plot` |
| Figure-example analysis | `analyze-plot` |
| Independent simulated review | `paper-review` |

If evidence is insufficient, determine whether it weakens the core claim. Route to `paper-writing` L0 Core Idea when it does; otherwise record a supporting-work task. Experiments are optional evidence, not a mandatory phase. Create result figures only from real results.

Choose the earliest unresolved dependency when several routes apply.

## Step 3: Checkpoint

Before invoking a specialist, create or update the project state in the **paper project** — never in the skill directory. Default path: `docs/systematic-research/plans/orchestrator-state.md`. Use [project-state.md](references/project-state.md) as a template.

Record: owner, objective, expected output, acceptance condition, and status `in progress`.

If the user only asks for routing advice without execution, answer in conversation — no state file needed.

## Step 4: Dispatch and Reconcile

Run the specialist skill and follow its gates. Parallelize only independent work; keep one owner per Section.

After the specialist finishes, update the **same** checkpoint with: actual output, gate result, affected work, and next action.

## Step 5: Recheck

When `paper-writing` Core Idea or Chapter Structure, evidence, figures, or venue changes, identify affected downstream work and revalidate it. Route review findings to the earliest responsible specialist stage instead of patching surface prose.

## Completion

Complete only when current decisions from `paper-writing` Core Idea and Chapter Structure are reflected in the paper, blocking findings are resolved, affected work has been rechecked, sources and results are not fabricated, known risks are visible, and the user confirms delivery.

## Guardrails

| Red flag | Route |
|---|---|
| “Write everything; find the thesis later.” | Route to `paper-writing` Core Idea. |
| “We can deliver while core empirical claims remain unverified.” | Record the required experiments; unverified core claims block delivery. |
| “Redo the brief despite an existing L0.” | Reuse the `paper-writing` Core Idea artifact. |
| “Two workers can rewrite one Section.” | Keep one owner. |
| “Fix the review by softening one sentence.” | Find the earliest faulty layer. |
| “Upstream changed; downstream is probably fine.” | Recheck affected work. |

# Research Orchestration Contract

Use this contract for research projects that cross more than one specialist skill.

## Default dependency order

`source corpus -> extracted evidence -> L0 thesis and venue -> L1 section and figure
plan -> paper and figures -> independent review -> accepted paper -> presentation`

Inspect existing sources and a draft in parallel when neither changes the other.
Resolve evidence gaps before accepting L0. `paper-writing` must lock a figure's
narrative job and required components in L1 before `paper-plot` begins P0. Start
`academic-pptx-skill` only from current, non-stale paper, figure, and evidence inputs.

`analyze-plot` is not a normal figure-production stage. Use it only when a reference
paper and its ground-truth figure or PPTX are available and the goal is to improve
general figure-design principles.

## Decision ownership

- Retrieval and `paper-extract` own source identity, source content, and evidence
  records; they do not define the paper's thesis.
- `paper-writing` owns thesis, contribution, venue, section logic, and each figure's
  narrative job; it consumes rather than rewrites source evidence.
- `paper-plot` owns visual encoding and layout within the accepted narrative job.
- `paper-review` owns independent findings; the earliest responsible owner resolves
  each finding.
- `academic-pptx-skill` owns presentation framing and slide construction while
  consuming accepted claims, evidence, and figures.

## Checkpoint record

Keep one row per artifact or decision with these fields:

- Artifact ID and version or content hash
- Produced by skill and stage
- Consumes artifact IDs and versions
- Accepted by and acceptance condition
- Status: missing, in progress, current, stale, blocked, or accepted risk
- Invalidation reason
- Output path and next action

## Invalidation

When an artifact changes, mark all reachable dependents stale before continuing.

- Source identity or extraction changes invalidate bibliography, evidence matrix,
  affected claims, L0/L1 decisions, prose, figures, reviews, and slides.
- Thesis or venue changes invalidate L1, paper skeleton, length constraints, figure
  narrative jobs and widths, reviewer framing, and deck framing.
- L1 changes invalidate dependent prose, figures, consistency audits, reviews, and
  slides.
- Figure changes invalidate text references, visual review findings, and slides that
  consume it.
- Review findings route to evidence, L0/L1, prose, experiments, or visuals according
  to ownership; Critical unresolved findings block delivery.

Revalidate stale artifacts in dependency order. Preserve superseded versions and
review history; do not silently overwrite the reason for rework.

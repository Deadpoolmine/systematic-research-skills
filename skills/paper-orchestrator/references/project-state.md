# Orchestrator State Template

Copy this template into the **paper project**. Never write runtime state into the installed skill directory.

Default project path: `docs/systematic-research/plans/orchestrator-state.md`.

If the project already has a planning directory, use that location and record it in the response.

```markdown
# Paper Orchestrator State

## Objective
- Deliverable:
- Language:
- Deadline:
- Venue: confirmed / candidate / undetermined
- Paper type: confirmed / candidate / undetermined

## Current Work
- Owner skill and stage:
- Objective:
- Expected output:
- Acceptance condition:
- Status: in progress / completed / blocked / revision required
- Next user decision:

## Result
- Actual output:
- Gate result: passed / failed / blocked
- Affected work:
- Next action:

## Artifacts
| Artifact | Project path | Status | Depends on |
|---|---|---|---|
| L0 | | missing/current/stale | |
| L1 | | missing/current/stale | L0 |
| Draft | | missing/current/stale | L0, L1 |
| Figures | | missing/current/stale | L0, L1, Draft |
| L3 audit | | missing/current/stale | Draft |
| Reviews | | missing/current/stale | Draft, Figures |

## Issues
| Finding | Source | Severity | Owner | Status |
|---|---|---|---|---|

## Decisions
| Decision | Reason | Affected artifacts | User confirmed |
|---|---|---|---|

## Backlog
| Work package | Owner | Output | Acceptance | Dependencies |
|---|---|---|---|---|

## Open Risks
- 

## Next Action
- 
```

Status meanings:

- `missing`: required but absent.
- `current`: validated against current inputs.
- `stale`: dependency changed; revalidation required.
- `blocked`: waiting for input or decision.
- `accepted-risk`: user accepted an unresolved non-Critical issue.

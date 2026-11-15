# Systematic Research Entrypoint Design

## Goal

Expose one canonical `systematic-research` entrypoint for the research suite while
preserving every specialist skill for direct triggering, reuse, and compatibility.

## Current Problem

The repository already contains `skills/systematic-research/SKILL.md`, but it owns
only retrieval and evidence verification. Clients recursively discover the sibling
skills and present the suite as unrelated entries. Adding a second orchestrator
named `paper-orchestrator` would create another peer instead of a clear front door.

## Upstream Design

`systematic-research` becomes the suite orchestrator and retains responsibility for
source retrieval. Its concise entry document will:

- inspect the user's goal and existing artifacts;
- route evidence discovery through its retrieval workflow;
- dispatch extraction, writing, review, plotting, plot analysis, and academic PPTX
  work to the existing specialist skills;
- record and re-evaluate dependencies when an upstream research decision changes;
- preserve the existing identity, provenance, and completion gates.

Detailed retrieval instructions move to an on-demand reference so `SKILL.md` stays
under the repository's 100-line target. Specialist directories and names do not
change. The proposed `paper-orchestrator` directory is therefore unnecessary.

## JoraX Integration

JoraX continues installing the complete repository so specialist skills remain
available. In the empty `/` menu, packaged entrypoints are ranked ahead of their
specialists and `systematic-research` is the visible suite entry. Once the user
types a query, matching specialist skills remain searchable and directly runnable.

The menu must derive this behavior from bundled-skill metadata rather than from the
order returned by OpenCode. Existing installations must keep working without data
migration; missing metadata falls back to the current flat catalog.

## Compatibility

- Existing `/systematic-research` invocations continue to perform evidence-led
  research and gain routing for broader research projects.
- Existing specialist names and file locations remain stable.
- Non-JoraX clients continue discovering all skills normally.
- JoraX does not hide specialist skills from explicit search.

## Verification

Upstream checks will validate frontmatter, the line-count convention, referenced
skill names, and retrieval script compatibility. JoraX checks will verify that the
empty slash menu contains `systematic-research`, does not flood the first page with
its sibling specialists, and that `/paper-writing` and other explicit searches still
return the specialist entry. The desktop app will be exercised against a seeded
workspace after the automated checks pass.

## Delivery

Submit the upstream change as a focused PR targeting `main`, disclose the model and
harness in its description, merge it after checks pass, then update JoraX's pinned
commit and menu metadata in a separate JoraX commit.

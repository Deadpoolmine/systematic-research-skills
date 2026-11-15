# Systematic Research Entrypoint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `systematic-research` the single default entrypoint for the research suite while retaining searchable specialist skills.

**Architecture:** The upstream entrypoint becomes a concise router and moves its detailed retrieval procedure into a reference file. JoraX pins the merged upstream revision and explicitly prioritizes suite entrypoints only for an empty slash query; typed searches continue using the complete OpenCode catalog.

**Tech Stack:** Markdown Agent Skills, Python `unittest`, TypeScript/React, Bun tests, Electron/OpenCode v2.

**Spec:** `docs/superpowers/specs/2026-11-15-systematic-research-entrypoint-design.md`

## Global Constraints

- The canonical public entrypoint name is exactly `systematic-research`.
- Do not add or ship a `paper-orchestrator` skill.
- Keep all existing specialist skill names and directories stable.
- Keep the entrypoint `SKILL.md` at or below 100 lines.
- Empty slash menus prioritize the suite entrypoint; explicit searches retain specialist skills.
- The upstream PR targets `main` and discloses GPT-5 Codex in the Codex desktop harness.

---

### Task 1: Upstream Systematic Research Router

**Files:**
- Modify: `skills/systematic-research/SKILL.md`
- Create: `skills/systematic-research/references/retrieval-workflow.md`
- Modify: `README.md`
- Create: `tests/test_skill_entrypoint.py`

**Interfaces:**
- Consumes: existing sibling skill names under `skills/`.
- Produces: a `systematic-research` entrypoint that routes to `paper-extract`, `paper-writing`, `paper-review`, `paper-plot`, `analyze-plot`, and `academic-pptx-skill`.

- [ ] **Step 1: Write the failing entrypoint contract test**

```python
def test_systematic_research_is_the_suite_entrypoint():
    text = ENTRYPOINT.read_text(encoding="utf-8")
    assert len(text.splitlines()) <= 100
    for skill in SPECIALISTS:
        assert f"`{skill}`" in text
    assert not (SKILLS / "paper-orchestrator").exists()
    assert (ENTRYPOINT.parent / "references" / "retrieval-workflow.md").is_file()
```

- [ ] **Step 2: Run the test and verify it fails**

Run: `python -m unittest tests.test_skill_entrypoint -v`
Expected: FAIL because the entrypoint does not reference every specialist and `retrieval-workflow.md` is absent.

- [ ] **Step 3: Move the detailed R0/E/R3 procedure into the retrieval reference and implement the concise router**

The entrypoint must inspect the request, choose the earliest unresolved research dependency, route it to one specialist, preserve the existing provenance hard gates, and recheck downstream outputs when upstream evidence or claims change.

- [ ] **Step 4: Update the README skill table**

List `systematic-research` first and describe it as the canonical suite entrypoint. Keep every specialist row.

- [ ] **Step 5: Run upstream verification**

Run: `python -m unittest discover -s tests -v`
Expected: all entrypoint and research-search tests PASS.

- [ ] **Step 6: Commit the upstream implementation**

```bash
git add skills/systematic-research README.md tests/test_skill_entrypoint.py
git commit -m "feat: make systematic research the suite entrypoint"
```

### Task 2: Upstream Pull Request and Merge

**Files:**
- No product files beyond Task 1.

**Interfaces:**
- Consumes: the tested upstream branch from Task 1.
- Produces: a merged `main` commit URL and SHA for JoraX pinning.

- [ ] **Step 1: Push the upstream branch and create the PR**

```bash
git push -u origin codex/systematic-research-entrypoint
gh pr create --base main --head codex/systematic-research-entrypoint
```

The PR body must summarize routing and compatibility, list the exact verification command, and disclose `GPT-5 Codex via Codex desktop`.

- [ ] **Step 2: Inspect required checks and diff**

Run: `gh pr checks --watch` and `gh pr diff --check` where supported.
Expected: all checks PASS and no unexpected specialist deletions appear.

- [ ] **Step 3: Merge the PR**

Run: `gh pr merge --squash --delete-branch`
Expected: PR reports `MERGED`; record the resulting `main` SHA.

### Task 3: JoraX Pin and Empty-Slash Prioritization

**Files:**
- Modify: `apps/desktop/resources/jorax/skills/systematic-research/systematic-research/SKILL.md`
- Create: `apps/desktop/resources/jorax/skills/systematic-research/systematic-research/references/retrieval-workflow.md`
- Modify: `apps/desktop/resources/jorax/skills/SOURCES.json`
- Modify: `apps/app/src/react-app/domains/session/surface/composer/slash-command.ts`
- Modify: `apps/app/src/react-app/domains/session/surface/composer/composer.tsx`
- Create: `apps/app/tests/jorax-featured-slash-skills.test.ts`

**Interfaces:**
- Consumes: `prioritizeEmptySlashItems(items, featuredNames, limit)` from `slash-command.ts`.
- Produces: an empty slash list with `systematic-research`, `microsoft-office`, and `ppt-master` before the normal catalog, while non-empty fuzzy queries remain unchanged.

- [ ] **Step 1: Write the failing slash-priority test**

```ts
test("empty slash menu promotes suite entrypoints without deleting specialists", () => {
  const result = prioritizeEmptySlashItems(items, ["systematic-research", "microsoft-office", "ppt-master"], 8);
  expect(result.map((item) => item.name).slice(0, 3)).toEqual(["systematic-research", "microsoft-office", "ppt-master"]);
  expect(items.some((item) => item.name === "paper-writing")).toBe(true);
});
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run: `pnpm --filter @openwork/app exec bun test tests/jorax-featured-slash-skills.test.ts`
Expected: FAIL because `prioritizeEmptySlashItems` is not exported.

- [ ] **Step 3: Implement stable empty-query prioritization**

Deduplicate featured names, preserve their configured order, append all remaining entries in engine order, and apply the existing limit. Keep `fuzzysort` unchanged for non-empty queries.

- [ ] **Step 4: Sync the merged upstream entrypoint and pin**

Copy the merged `SKILL.md` and `references/retrieval-workflow.md` into the bundled systematic-research directory, then set its `SOURCES.json` commit to the merged upstream SHA. Do not alter other bundled skills.

- [ ] **Step 5: Run JoraX verification**

Run:

```bash
pnpm --filter @openwork/app exec bun test tests/jorax-featured-slash-skills.test.ts
pnpm --filter @openwork/app typecheck
node --test apps/desktop/test/jorax-skill-seed.test.mjs
```

Expected: all tests PASS and TypeScript reports no errors.

- [ ] **Step 6: Verify the actual desktop menu**

Start the existing JoraX desktop development profile, open a new task, type `/`, and confirm `systematic-research` is visible. Type `/paper-writing` and confirm the specialist remains visible.

- [ ] **Step 7: Commit and push JoraX**

```bash
git add apps/app/src/react-app/domains/session/surface/composer apps/app/tests/jorax-featured-slash-skills.test.ts apps/desktop/resources/jorax/skills
git commit -m "feat: promote bundled skill entrypoints"
git push origin jorax-dev
```

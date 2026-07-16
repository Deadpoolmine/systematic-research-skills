# L3 — Consistency Check Stream (The Auditor Phase)

**Load when:** executing L3 (write or polish). Systematic cross-validation protocol.

**REQUIRED BACKGROUND:** SKILL.md hard gates. L2 complete.

## Checklist

All 7 checks must pass. Checks 1-6 validate **structure**; Check 7 validates **prose quality**.

### Structural Checks (1-6)

| # | Check | Method | Pass Condition |
|---|-------|--------|---------------|
| 1 | **Thesis Trace** | Every Section claim maps to ≥1 L0 core point | No orphan claims |
| 2 | **Design Coverage** | All L0 design points (#5) appear in L2 | 100% coverage |
| 3 | **Challenge-Response** | Introduction challenge matches L0 #3 | Exact or equivalent |
| 4 | **Result Consistency** | L2 results match L0 #6 summary | No contradiction; draft mode: setup consistent + [TODO] markers present |
| 5 | **Section Contract** | Each Section fulfills its L1 A→B→C chain | All chain items addressed |
| 6 | **Contribution Alignment** | Contributions = L0 design points + key results | No extras, no omissions |

### Prose Quality Check (7) — Fine-Grained Line-by-Line Polish

**Read the ENTIRE paper linearly, sentence by sentence. Do NOT skip or skim.**

<HARD-GATE-L3-PROSE>
Check 7 MUST be performed by reading the full paper from abstract to conclusion, in order.
Do NOT check by Section in isolation — read across Section boundaries.
After sub-checks 7a-7g pass, perform a SECOND dedicated pass for length only: split every paragraph > 6 sentences and every sentence > 30 words.
</HARD-GATE-L3-PROSE>

| Sub-Check | What to Verify | Fix Action |
|-----------|---------------|------------|
| **7a. Sentence length** | Hard cap: 30 words. Flag every sentence > 25 words. No run-ons. | Split at nearest clause boundary |
| **7b. Paragraph length** | Hard cap: 6 sentences. Flag every paragraph > 5 sentences. One idea = one chain step. | Split at logical break; if impossible, the L1 chain step is too broad |
| **7c. Conciseness** | Every sentence earns its place. Remove: filler ("it is worth noting", "interestingly", "in particular"), redundant clauses, hedging ("may potentially", "could possibly"). | Cut in-place |
| **7d. Paragraph structure** | Every paragraph = topic → support → conclude/transition (总分总). First sentence declares point. | Restructure if topic sentence buried |
| **7e. Inter-paragraph flow** | Each paragraph's last sentence bridges to next paragraph's topic. No jumps. | Add transition or reorder |
| **7f. Vocabulary** | No obscure words. Replace: ameliorate→improve, delineate→describe, elucidate→explain, heretofore→previously, utilize→use, facilitate→help, leverage→use, mitigate→reduce, paradigm→approach, efficacy→effectiveness. | Replace in-place |
| **7g. Pronoun clarity** | Every "this", "it", "they" has an unambiguous antecedent in same or previous sentence. | Replace with explicit noun |

**Execution:** Read linearly. Fix each issue immediately before moving to next sentence. After full pass, do a dedicated second pass checking ONLY 7a + 7b — split long sentences and paragraphs ruthlessly. Then re-read once more to verify fixes didn't break flow.

## Draft Mode (Check #4)

If L0 #6 status = "In progress": verify setup matches L0, [TODO] markers present, no unmarked fabricated numbers. Relaxed — pass with note.

## Resolution Protocol

For each issue: identify **root cause** (L0 omission? L1 gap? L2 drift?). Fix at earliest level. Re-run all 6 checks after fixes.

## Report Format

```markdown
## L3 Consistency Report — <Topic>

### ✅ Structural (Checks 1-6)
- Check 1: all claims trace to L0
- Check 4: draft mode — setup consistent, [TODO] marked

### ⚠️ Structural Issues
- Check 2: DP2 not covered → root: L1 Design chain omitted DP2 → fix L1, re-draft L2

### ✅ Prose Quality (Check 7)
- 7a: 5 sentences > 30 words split
- 7b: 3 paragraphs > 6 sentences split
- 7c: 12 filler phrases removed
- 7d: 2 paragraphs restructured (topic sentence buried)
- 7e: 4 transitions added between paragraphs
- 7f: 10 obscure words replaced
- 7g: 6 ambiguous pronouns clarified
```

## Transition

All checks pass → commit `paper/` with `L3: final for <topic>`.

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
</HARD-GATE-L3-PROSE>

| Sub-Check | What to Verify | Fix Action |
|-----------|---------------|------------|
| **7a. Conciseness** | Every sentence earns its place. Remove: filler words, redundant clauses, "it is worth noting that...", "interestingly..." | Cut or merge |
| **7b. Paragraph structure** | Every paragraph = topic → support → conclude/transition (总分 or 总分总). First sentence declares point. | Restructure if topic sentence buried or missing |
| **7c. Inter-paragraph flow** | Each paragraph's last sentence bridges to the next paragraph's topic. No jarring jumps. | Add transition sentence or reorder paragraphs |
| **7d. Vocabulary** | No obscure words. Replace: ameliorate→improve, delineate→describe, elucidate→explain, heretofore→previously, utilize→use, facilitate→help/enable, leverage→use. | Replace in-place |
| **7e. Sentence variety** | Mix short (8-12 words) and long (18-25 words). No 3+ long sentences in a row. | Split or combine |
| **7f. Pronoun clarity** | Every "this", "it", "they" has an unambiguous antecedent within the same or previous sentence. | Replace with explicit noun |
| **7g. Redundancy** | No sentence repeats what the previous sentence already said in different words. | Delete the weaker version |

**Execution:** Read linearly. Fix each issue immediately before moving to the next sentence. After full pass, re-read once more to verify fixes didn't break flow.

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
- 7a: 12 filler phrases removed
- 7b: 3 paragraphs restructured (topic sentence buried)
- 7c: 2 transitions added between Sections
- 7d: 8 obscure words replaced
- 7e: 5 long sentences split
- 7f: 4 ambiguous pronouns clarified
- 7g: 2 redundant sentences deleted
```

## Transition

All checks pass → commit `paper/` with `L3: final for <topic>`.

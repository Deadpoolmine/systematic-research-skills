# L3 — Consistency Check Stream (The Auditor Phase)

**Load when:** executing L3 (write or polish). Systematic cross-validation protocol.

**REQUIRED BACKGROUND:** SKILL.md hard gates. L2 complete.

## Checklist

Run all 6 checks. All must pass. Produce full report.

| # | Check | Method | Pass Condition |
|---|-------|--------|---------------|
| 1 | **Thesis Trace** | Every Section claim maps to ≥1 L0 core point | No orphan claims |
| 2 | **Design Coverage** | All L0 design points (#5) appear in L2 | 100% coverage |
| 3 | **Challenge-Response** | Introduction challenge matches L0 #3 | Exact or equivalent |
| 4 | **Result Consistency** | L2 results match L0 #6 summary | No contradiction; draft mode: setup consistent + [TODO] markers present |
| 5 | **Section Contract** | Each Section fulfills its L1 A→B→C chain | All chain items addressed |
| 6 | **Contribution Alignment** | Contributions = L0 design points + key results | No extras, no omissions |

## Draft Mode (Check #4)

If L0 #6 status = "In progress": verify setup matches L0, [TODO] markers present, no unmarked fabricated numbers. Relaxed — pass with note.

## Resolution Protocol

For each issue: identify **root cause** (L0 omission? L1 gap? L2 drift?). Fix at earliest level. Re-run all 6 checks after fixes.

## Report Format

```markdown
## L3 Consistency Report — <Topic>

### ✅ Passing
- Check 1: all claims trace to L0
- Check 4: draft mode — setup consistent, [TODO] marked

### ⚠️ Issues
- Check 2: DP2 not covered → root: L1 Design chain omitted DP2 → fix L1, re-draft L2
```

## Transition

All checks pass → commit `paper/` with `L3: final for <topic>`.

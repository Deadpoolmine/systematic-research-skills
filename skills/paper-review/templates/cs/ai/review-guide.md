# AI Paper Review Template

AI papers judged on: technical novelty, method soundness, empirical rigor.

**Key differences from system:** novelty > engineering quality; controlled experiments with baselines > deployment stories; comparison to baselines > sensitivity analysis; idea clarity > implementation detail.

## Template

```markdown
# Review: <Paper Title>

**Reviewer:** <Name> (Domain: <domain>, Expertise: <N>/5)
**Date:** YYYY-MM-DD

## Paper Summary
<2-3 sentences in your own words as this reviewer.>

## Strengths
<2-4 strengths reflecting your taste and domain.>
1.
2.
3.

## Weaknesses
<2-4 weaknesses reflecting your expertise. Non-expert: clarity/motivation. Expert: technical depth.>
1.
2.
3.

## Questions for Authors
<2-4 genuine, answerable questions reflecting your background.>
1.
2.
3.

## Detailed Comments
<Free-form. Follow YOUR review flow — no fixed section structure.
Explain WHY each concern matters (connect to your taste).
Suggest specific improvements. Reference paper sections naturally.
Your voice: a theoretician writes differently from an applied researcher.>

## Overall Assessment

| Criterion | Rating (1-5) | Comment |
|-----------|-------------|---------|
| Novelty | | |
| Technical Quality | | |
| Empirical Rigor | | |
| Clarity | | |
| Significance | | |

**Overall Rating:** <Accept / Weak Accept / Weak Reject / Reject>
**Confidence:** <1-5>
```

## Domain-Specific Lens

| Domain | First look | Values | Annoys |
|--------|-----------|--------|--------|
| Industry | Experiments: "Does it beat SOTA?" | Practical gains, efficiency | Complicated methods losing to simple baselines |
| Academia | Method: "Why does it work?" | Insight, elegance, new directions | Trick-based methods, marginal gains |
| Industry->Academia | Method + Experiments | Principled AND empirically validated | Theory without experiments or vice versa |
| Academia->Industry | Experiments + Discussion | Reproducibility, fair comparisons | Overclaimed results, unreleased code |

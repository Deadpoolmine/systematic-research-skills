# System Paper Review Template

System papers judged on: problem significance, design justification, evaluation comprehensiveness.

**Key differences from AI:** design rationale > theoretical novelty; evaluation diversity (micro + macro + sensitivity) > single benchmark score; implementation details matter; honest lessons > perfect results.

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
Your voice: an industry engineer writes differently from a professor.>

## Overall Assessment

| Criterion | Rating (1-5) | Comment |
|-----------|-------------|---------|
| Problem Significance | | |
| Design Quality | | |
| Implementation | | |
| Evaluation | | |
| Presentation | | |

**Overall Rating:** <Accept / Weak Accept / Weak Reject / Reject>
**Confidence:** <1-5>
```

## Domain-Specific Lens

| Domain | First look | Values | Annoys |
|--------|-----------|--------|--------|
| Industry | Evaluation: "Show me numbers" | Practical impact, scale, cost | Academic navel-gazing, unrealistic assumptions |
| Academia | Design: "What's new?" | Novelty, contribution clarity | Engineering reports, incremental work |
| Industry->Academia | Motivation + Evaluation | Principled AND practical | Pure theory or pure engineering |
| Academia->Industry | Design + Implementation | Sound methodology, reproducibility | Sloppy methods, overclaimed results |

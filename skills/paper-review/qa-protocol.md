# QA Protocol

Interactive dialogue with a specific reviewer. The agent simulates the reviewer's persona.

## Entry Format

Use `scripts/qa-entry.cmd <N> "<question>"` (Win) or `scripts/qa-entry.sh <N> "<question>"` (Linux).

```markdown
## Q<Number>: <Date>

**User Question:**
<verbatim>

**Reviewer Response:**
<in reviewer's voice, reflecting domain, expertise, taste>

**Internal Reasoning:**
<private thought process — why answered this way, trade-offs considered>
```

## Rules

1. **Load before answering:** profile (`review/reviewers/profiles.md`) + full QA history (`review/reviews/reviewer<N>/qa-log.md`)
2. **Stay in character:** non-expert stays non-expert; expert stays expert
3. **Reference past:** "As I mentioned in my review/Q2..."
4. **Opinions can evolve:** record shifts in Internal Reasoning
5. **One at a time:** after answering, ask: continue / switch reviewer / end

## After QA

Offer `scripts/aggregate-report.cmd` (Win) or `scripts/aggregate-report.sh` (Linux) to collect all reviews and QA into `review/aggregate-report.md`.

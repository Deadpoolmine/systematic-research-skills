# Speaker Notes

## Contents

1. Notes artifact
2. Per-slide schema
3. Timing
4. Verification
5. Conference and defense delivery
6. Q&A preparation

## 1. Notes Artifact

The bundled converter does not require notes to be embedded in PowerPoint. Create a sidecar `speaker-notes.txt` in `artifacts/` when the user requests a script, when external sources were researched, or when timing and Q&A preparation materially improve delivery.

Keep visible slide copy concise. Put transitions, interpretation, definitions, caveats, and optional detail in notes. Do not place a claim in notes that contradicts or exceeds the verified evidence.

## 2. Per-Slide Schema

```text
Slide [N] - [Takeaway title]
Purpose: [what the audience should understand]
Time: [seconds]

Talk track:
[Natural spoken text. Do not read the slide verbatim.]

Transition:
[One sentence linking to the next question.]

Presenter cues:
- [Point to panel B / pause / define term / skip if short on time]

Likely question:
- Q: [question]
  A: [evidence-grounded answer or backup-slide pointer]

[Sources]
- [E03] [Full source and locator; what it supports]
```

The `[Sources]` block is mandatory for external visuals and non-trivial externally sourced claims. It is provenance, not spoken text.

## 3. Timing

Budget time by complexity, not uniformly:

- cover: 15-30 seconds;
- motivation/gap: 35-60 seconds;
- method diagram: 45-90 seconds;
- central result: 60-120 seconds;
- secondary result: 40-75 seconds;
- limitations: 35-60 seconds;
- close: 30-60 seconds.

Keep 5-10 percent of the speaking slot as contingency. Mark optional details that can be skipped without breaking the argument. If the script exceeds the slot, remove content or slides before accelerating delivery.

## 4. Verification

After drafting `artifacts/speaker-notes.txt`, verify structure and timing:

```bash
node "<SKILL_DIR>/scripts/verify-speaker-notes.cjs" \
  "<WORKSPACE_DIR>/artifacts/speaker-notes.txt" \
  --slides 15 \
  --language en \
  --min-minutes 12 \
  --max-minutes 15 \
  --json "<WORKSPACE_DIR>/artifacts/speaker-notes-report.json"
```

Adapt the slide count, language, and timing window to the actual task. Use the report to check:

- slide numbering is continuous and matches the deck;
- every slide has a `Purpose`, `Time`, `Talk track`, and `Transition`;
- total word count is consistent with the intended pace;
- English-only notes contain no unintended CJK spillover;
- optional source blocks and likely-question coverage are present where needed.

Treat the duration estimates at 120, 130, and 140 words per minute as planning bounds, not guarantees. If the script is too short, add explanation or transitions; if it is too long, cut content before speaking faster.
Pass `-` instead of a file path to validate notes supplied through standard input during a quick draft check.

## 5. Conference And Defense Delivery

### Conference Or Seminar

Write for oral clarity. Introduce technical terms immediately before they are needed. Emphasize the single visual finding and its implication. Use transitions to maintain momentum; avoid reading methods lists or table cells.

### Defense

Make definitions, scope, assumptions, validity, and contribution boundaries explicit. Anticipate why a method was selected, what alternatives were rejected, and what evidence supports novelty. Keep answers measured; distinguish what the work demonstrates from what remains a hypothesis.

Use the user's requested language. When slides and speech use different languages, preserve technical terms consistently and record the bilingual mapping once.

## 6. Q&A Preparation

Build a question matrix around:

- novelty and relation to prior work;
- data representativeness, missingness, and ethics;
- baseline choice and fairness of comparison;
- statistical power, uncertainty, and robustness;
- assumptions and alternative explanations;
- generalization and failure cases;
- reproducibility and implementation detail;
- practical or theoretical implications.

Point answers to verified evidence or backup slides. If the evidence is absent, say so directly and frame it as future work rather than improvising a result.

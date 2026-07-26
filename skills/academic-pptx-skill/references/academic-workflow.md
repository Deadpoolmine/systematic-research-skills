# Academic Workflow

## Contents

1. Intake contract
2. Source reading pass
3. Conference and seminar talks
4. Thesis, proposal, and dissertation defenses
5. Slide planning schema
6. Appendix strategy

## 1. Intake Contract

Resolve these variables before outlining:

| Variable | Record |
|---|---|
| Format | Conference talk, invited seminar, group meeting, proposal defense, thesis defense, or dissertation defense |
| Audience | Specialists, mixed field, committee, students, or public-academic |
| Duration | Total speaking time and whether Q&A is included |
| Language | Visible slides and spoken language; they may differ |
| Source boundary | User-supplied only, or external research allowed |
| Required content | Claims, figures, sections, disclosures, acknowledgements |
| Evaluation goal | Understanding, technical scrutiny, approval, or discussion |

When the user does not specify a duration, do not fabricate an institutional rule. Use a working assumption and label it in the plan.

## 2. Source Reading Pass

When the source is a paper, manuscript, report, or thesis chapter, do not skim randomly. Rebuild the argument in an order that supports slide selection:

1. Abstract and introduction: extract the one-sentence problem, the one-sentence idea, and the headline result.
2. Background or framing: isolate the minimum concepts the audience must know before the method.
3. Motivation or observation: find the evidence that makes the design or hypothesis necessary.
4. Method or design: extract modules, assumptions, inputs, outputs, implementation constraints, and validity-critical details.
5. Evaluation or findings: extract setup, baselines, datasets, workloads, metrics, exact numbers, uncertainty, and limitations.
6. Conclusion and explicit limitations: identify what the work demonstrates, and what it does not justify overclaiming.

While reading, distinguish:

- theoretical maxima versus measured results;
- observed outcomes versus planned future work;
- normalized values versus raw units;
- mechanism claims versus interpretation.

Record every reusable number, figure, and boundary condition in the evidence ledger before outlining slides.

## 3. Conference And Seminar Talks

### Narrative Arc

Use a question-led arc:

1. Why this problem matters to this audience.
2. What precise gap remains.
3. What question or hypothesis is tested.
4. What the proposed method changes.
5. What the strongest result shows.
6. Why that result is credible.
7. What the result changes, and what remains unresolved.

Open quickly. Do not reproduce the paper's section order mechanically. A talk is an argument supported by selected evidence, not a compressed manuscript.

### Default Pacing

Use roughly one substantive slide per minute, then adjust for figure complexity and audience expertise.

| Duration | Typical main-deck range | Suggested allocation |
|---|---:|---|
| 8-10 min | 8-11 slides | 1 opening, 2 motivation/gap, 2 method, 2-3 results, 1 interpretation, 1 close |
| 12-15 min | 11-15 slides | 1 opening, 3 context/gap, 3 method, 3-4 results, 1 limitations, 1 close |
| 20 min | 15-20 slides | 1 opening, 3-4 context/gap, 4 method, 5-6 results, 1 limitations, 1 close |

Do not force a table of contents into a short talk. Use a verbal roadmap or a single compact orientation slide only when the structure is genuinely complex.

### Result Selection

Choose results by argumentative value:

- primary outcome or central finding;
- comparison against the strongest relevant baseline;
- uncertainty, robustness, or ablation needed to establish credibility;
- one example or failure case that reveals mechanism or boundary conditions.

Move exhaustive benchmarks and secondary metrics to backup slides.

## 4. Thesis, Proposal, And Dissertation Defenses

### Narrative Arc

Use an evaluation-led arc:

1. Research problem and scope.
2. Literature boundary and unresolved gap.
3. Research questions, hypotheses, or objectives.
4. Overall research framework.
5. Methods, data, assumptions, and validity controls.
6. Findings organized by research question or contribution.
7. Cross-finding synthesis and contribution claim.
8. Limitations, threats to validity, and future work.
9. Final answer to the original research question.

For proposal defenses, replace completed findings with expected evidence, feasibility, milestones, and risk controls. Never present planned outcomes as observed results.

### Default Pacing

| Duration | Typical main-deck range | Emphasis |
|---|---:|---|
| 15 min | 13-17 slides | Central question, method credibility, strongest findings |
| 20 min | 17-22 slides | Balanced problem, method, findings, contributions |
| 30 min | 22-30 slides | More validation, synthesis, limitations, and contribution detail |

Institutional rules override these defaults. Reserve Q&A backup slides outside the timed main sequence.

### Committee-Oriented Content

Make these explicit when relevant:

- research scope and excluded scope;
- operational definitions;
- data provenance and ethics;
- assumptions and threats to validity;
- why each method answers the stated question;
- what is genuinely new versus adapted or integrated;
- evidence supporting each contribution;
- known failure modes and limits of generalization.

Do not hide limitations in the appendix. A concise main-deck limitations slide increases credibility.

## 5. Slide Planning Schema

For each slide record:

```text
Slide: [N]
Role: [opening / gap / question / method / result / synthesis / limitation / close / backup]
Claim: [one complete takeaway sentence]
Evidence: [E03, F02, T01]
Visual: [figure, chart, equation, process, table, or text-led]
Visible copy: [short phrases only]
Transition in: [question answered from previous slide]
Speaking time: [seconds]
Risk: [source gap, dense visual, terminology, or none]
```

Check that the sequence is cumulative. Every method slide should enable a result slide; every result slide should support a conclusion; every contribution claim should point back to evidence.

## 6. Appendix Strategy

Use backup slides for material likely to matter in Q&A but too detailed for the main story:

- full derivations and proofs;
- hyperparameters and implementation details;
- additional baselines and robustness checks;
- complete survey instruments or coding schemes;
- ethics approvals and data governance detail;
- negative results and edge cases;
- definitions and supplementary literature mapping.

Number appendix slides continuously or prefix them clearly. Preserve the same visual system and citations. Do not use the appendix to conceal evidence required for a main-deck claim.

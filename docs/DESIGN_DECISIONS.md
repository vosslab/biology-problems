# Design decisions

<!-- VENDORED HEADER: START -->
Record each durable decision about how this code and repository are shaped, once it is settled, with
the reasoning a later reader needs. Guidance Neil Voss states belongs in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), dated history in `docs/CHANGELOG.md`, open discussion in
`docs/active_plans/decisions/`. [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

Write each decision as a level-three heading with these four fields. `Owner` names the
authoritative code or contract document, rather than a person.

```markdown
### <decision title>

**Decision.** <the durable direction>

**Why.** <the reason it was chosen>

**Consequence.** <the constraint a future change preserves>

**Owner.** <the authoritative code or contract doc>
```

## Software design

### Restriction-digest cut placement

**Decision.** Restriction-digest questions keep one map-and-gel format.
Placement proposes mixed, readable maps. Evaluation checks validity, then
the mode's required answer shape. At most half of the correct distinct
bands may also appear in the distractor digest
(`shared_correct_fraction <= 0.5`). Difficulty is the fragment list and
distinct-band set. Full rules live in
[CUT_PLACEMENT.md](../problems/molecular_biology-problems/restriction_enzymes/CUT_PLACEMENT.md).

**Why.** Two circular cuts produce only complementary sizes `{d, L-d}`, so
raising length with two sites per enzyme leaves the reasoning unchanged.
The key comes from the named enzyme alone. Rigorous items use co-migrating
equal fragments as one band.

**Consequence.** Update
[CUT_PLACEMENT.md](../problems/molecular_biology-problems/restriction_enzymes/CUT_PLACEMENT.md)
first, then the generators.

**Owner.** [CUT_PLACEMENT.md](../problems/molecular_biology-problems/restriction_enzymes/CUT_PLACEMENT.md)

### Question-writing guides are canonical here

**Decision.** Rules for student-facing question text live in canonical files in this
repository: [QUESTION_PEDAGOGY_GUIDE.md](QUESTION_PEDAGOGY_GUIDE.md) (design and review),
[QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md) (wording and format),
[QUESTION_EXEMPLARS.md](QUESTION_EXEMPLARS.md) (examples that cite rules), and
[QUESTION_EVIDENCE.md](QUESTION_EVIDENCE.md) (corpus audit and verified research behind the
rules). Each rule lives in one file. The `bptools-writer-expert` and `webwork-writer-expert`
skills bundle byte-identical snapshots of all four under `references/docs/`, so the evidence
travels with the skills instead of sitting behind a repo path.

**Why.** Generators and PGML problems both live here, and agents without either skill read
`AGENTS.md`; one canonical home keeps the skills and the repository from drifting apart.

**Consequence.** Edit the canonical file first, then refresh both skill snapshots in the same
change. Other authoring guides link to these rules instead of restating them.

**Owner.** [QUESTION_PEDAGOGY_GUIDE.md](QUESTION_PEDAGOGY_GUIDE.md)

### Pedigree terminal-frontier metadata stays transient

**Decision.** The terminal-frontier constructor reserves the final family slots before constructing
the connecting generations. Designated IDs stay outside biological simulation, `Family`, rendering,
and cache records. Validate planned geometry before biology, validate displayed endpoints after
acceptance, and roll back a repair or polish proposal if it breaks those endpoints.

**Why.** The measured question concerns family shape and rendered endpoint placement. Keeping
designation out of biology preserves existing inheritance and teaching rules, while checking the
actual `Diagram` protects the displayed contract after layout and polishing.

**Consequence.** Keep frontier metadata local to candidate generation and preserve the accepted input
when a topology-changing stage breaks endpoint validity. Treat workload enablement as a separate
evidence-based policy decision.

**Owner.** [PEDIGREE_PIPELINE.md](../problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md)

### Enable terminal frontiers for bonus identification

**Decision.** Use the terminal-frontier constructor for bonus identification only, sampling 9 or 10
terminal families. Keep easy identification, selection, matching, and other difficulty levels on
their existing constructor. Keep polishing and current acceptance gates.

**Why.** The 100-target comparison found no easy construction gain and lower median pre-polish
bottom-empty space for bonus. One reviewer preferred the frontier in four of five blinded bonus
pairs, with one exception. The sample is moderate and does not measure student outcomes.

**Consequence.** Treat frontier construction as a narrow bonus workload choice. Do not claim that it
removes the need for polishing or improves student learning. Revisit the scope only with meaningful
new evidence.

**Owner.** [PEDIGREE_DIFFICULTY.md](../problems/inheritance-problems/pedigrees/PEDIGREE_DIFFICULTY.md)



## Dependencies

## Generated artifacts

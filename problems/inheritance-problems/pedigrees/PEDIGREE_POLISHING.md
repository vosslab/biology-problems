# Pedigree geometric repair and polishing

The production pipeline has two bounded stages: geometry-first downward repair, then ordinary
biological polishing. Their placement in the overall flow is described in
[PEDIGREE_PIPELINE.md](PEDIGREE_PIPELINE.md). The measured geometry contract is in
[PEDIGREE_LAYOUT.md](PEDIGREE_LAYOUT.md).

## Downward repair

[downward_repair.py](pedigree_lib/downward_repair.py) acts on any generated family that fits the
rigorous workload (including pattern-to-pedigree and selection pools); it returns other workloads
unchanged. It requires sampled genotypes. If largest bottom-anchored empty fraction `E`
exceeds 12%, it proposes a geometry-improving child addition to an existing union or promotes an
eligible uncoupled nonterminal person by adding a mate and child. Geometry chooses the placement
before Mendelian state is sampled. Each new person is sampled once; rejected proposals are not
rerolled. The repair preserves original people and relationships and never exceeds 26 people or
five generations.

Repair stops at or below 12%, when no legal geometry improvement remains, when the first sampled
proposal fails a required acceptance gate, or when the family reaches capacity. The target is
best-effort, not guaranteed. The 12% trigger and stopping target are production constants; they are
not calibrated quality thresholds. See [PEDIGREE_EVIDENCE.md](PEDIGREE_EVIDENCE.md) for the
historical geometry results, production-order comparison, and limitations.

## Ordinary polishing

[polishing.py](pedigree_lib/polishing.py) then runs for every preset and format, trying at most two
terminal-child additions to shrinking rows after generation II. Each proposal preserves original people, observations,
genotypes, and relationships. Added genotypes must be possible parental transmissions. A proposal
must pass current biology, teaching, affected-sex balance, layout, and difficulty checks; preserve
the answer, teaching profiles, and compatible modes; reduce mean shrink; and avoid greater width or
lower progression.

The polisher samples sex fairly, chooses the best structural placement by progression minus mean
row density, then samples one genotype from weighted Mendelian transmissions. Affected reach and
affected-distribution preferences do not choose the child's outcome. Failure stops the stage without
rerolling; if no proposal qualifies, the original accepted case is returned. Cases with no change
remain eligible. Diagnostic affected-sex counts may change while teaching profiles stay intact, so
requiring identical diagnostic text would reject valid additions.

## Interpretation

Acceptance filters condition the displayed sample; generated families are not an unbiased population
simulation. The local bank stores accepted procedural families, not review artifacts. Ranking keeps
the outside-affected-reach preference separate from the child outcome. Neither stage uses LLM review.
One-time replay results and their limits are summarized in
[PEDIGREE_EVIDENCE.md](PEDIGREE_EVIDENCE.md) and recorded with dated decisions in the changelog;
they are not guarantees about future samples.

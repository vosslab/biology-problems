# Plan: Ship the pedigree polisher and sorter

## Context

Pedigree aesthetics work has produced several useful individual measurements, a bounded
polisher, and a tested bottom-empty-space repair. The current production sorter is a simple
weighted combination, but the combined weighting remains unproven. A retrospective comparison
on the existing 1,000-rated top-pool corpus supports using a simple equal-rank combination as
the next production sorter. The observed gain is modest and reversible; this is sufficient to
ship a practical candidate ordering while preserving the underlying measurements for later
revision.

The bottom-empty-space experiment used a historical 22.58% cutoff. That value marked the
development cohort's upper quartile and was not a visual acceptability boundary. The user has
chosen 12% (approximately one eighth) as both the repair entry trigger and completion target:
begin repair when the normalized largest bottom-anchored empty rectangle exceeds 0.12, and stop
when it is at or below 0.12.

## Goal

Integrate the best currently supported bounded polisher and candidate sorter into the normal
pedigree generation pipeline, document the evidence and limits, verify the three question
workflows, and close the aesthetics investigation.

## Settled decisions

### Pipeline order

Use this order for fresh generated pedigrees:

```text
generate valid candidate
  -> repair large bottom-anchored empty space when eligible
  -> run the existing bounded biological polisher
  -> apply the existing difficulty and teaching acceptance checks
  -> rank the eligible pool
  -> assemble ordinary question scenarios
```

The matched two-replicate comparison on the preserved 100 rigorous sources modestly favored
repair before ordinary polishing. Repair reached the 12% target in 40/200 runs versus 34/200
for the reverse order; mean final empty fraction was 0.184997 versus 0.189106. Both orders
changed 111/200 runs, and both preserved the measured biological and teaching invariants. Ordinary
polishing after repair moved the empty fraction upward in two runs by 0.003233, but no run that
had reached the 12% target crossed back above it. The comparison found no reason to add an
interaction rollback gate.

### Repair trigger and target

Use one fixed internal value, `0.12`, for both roles:

- Start downward repair when the largest bottom-anchored empty rectangle occupies more than
  12% of the tight pedigree content bounding-box area.
- Stop repair when the fraction is 12% or lower, when the workload's person capacity is full,
  or when no accepted geometry-improving edit remains.

The metric describes one largest bottom-anchored empty rectangle; it does not measure the
percentage of visible white pixels. The old 22.58% development-quartile value remains historical
pilot evidence, not a production threshold.

### Workload eligibility

Apply downward repair to the rigorous workload defined by the shared difficulty authority, not
by question-script name. This is the five-generation, 23-26-person rigorous pedigree workload
with its existing founder, couple, and sibship bounds. Question forms with that workload qualify
automatically. Smaller matching workloads continue through the ordinary polisher and sorter.
The eligibility check belongs with shared difficulty policy so future workflows inherit the
workload decision consistently.

### Repair behavior

Port the existing bounded geometry-first repair into the production pedigree library. Retain its
two demonstrated operations: add a child to an existing union, or promote an eligible uncoupled
nonterminal individual by adding a mate and child. Use geometry and structure to choose a location
before sampling biological states. Sample each proposed Mendelian outcome once, then run the full
existing biological, teaching, difficulty, and layout checks. Preserve the last accepted state
when a sampled proposal fails. Respect the rigorous workload's current 26-person ceiling and
five-generation structure.

Run repair before the existing bounded polisher because both use the same remaining person
capacity. Keep the ordinary polisher behavior intact and calculate the final ranking only after
both polishing stages.

### Candidate sorter

Replace the current pool ordering score with the equal mean of five favorable percentile ranks
calculated within the current eligible pool:

1. Lower outside affected-reach fraction.
2. Higher affected-region fill, using the existing native 2-generation by 4-sibling-pitch
   region measurement.
3. Higher generation progression.
4. Lower mean row density.
5. Lower excess bottom-empty fraction, `max(0, E - 0.12)`; candidates at or below the target
   receive equal credit on this component.

Use average midranks for ties and preserve randomized pool order for equal final scores. Give each
signal one equal vote; use no fitted weights. When a signal is constant in the current pool, its
midrank gives all cases equal credit. Recompute ranks whenever the candidate pool changes. Keep
the score attached to the ranked case only for that pool, and do not store it in the persistent
pedigree cache.

The score is an ordering aid among already accepted candidates. It is not a validity test and
does not repeatedly resample genetic outcomes.

## Evidence and limits

The equal-five ranking was recomputed from the frozen development/validation split of the
existing 1,000 reviewed pedigrees. At the top quartile, its mean overall rating was 3.888 versus
3.824 for the old score in development, and 3.928 versus 3.888 in validation. Mode-balanced
top-quartile means were 3.781 versus 3.728 in development and 3.851 versus 3.845 in validation.
Readability was slightly lower for equal-five in both pooled splits. These retrospective results
support shipping a simple reversible sorter; they do not prove prospective improvement or
independent generalization.

The ordering comparison reused 100 preserved rigorous sources with two fixed replay seeds. It
was a geometric and invariant comparison; changed pedigrees did not receive new blind ratings.
The earlier blind pilot at the 22.58% cutoff rated 13 changed pedigrees and found a modest mean
overall improvement among changed cases. The new 12% target has not received its own blind
review. Keep these differences clear in documentation.

No additional calibration corpus, rubric change, or blind-review campaign is part of this
close-out. Existing experiment reports remain the evidence archive under the sibling
`pedigree-aesthetics` workspace.

## Implementation boundaries

- Keep feature measurement, bottom-space measurement/repair, and pool ranking in small,
  separately replaceable pedigree-library modules.
- Keep score fields pool-relative and recomputable. Cache storage continues to hold pedigree
  source data; it does not hold ranking scores.
- Revalidate cached candidates, calculate current geometry and measurements, and rank them with
  fresh candidates in the same pool.
- Preserve existing question assembly rules: identification uses accepted singletons; selection
  and matching retain all five modes and their existing shared workload grouping.
- Keep instructor review output's score and feature fields truthful to the new sorter.
- Keep permanent tests to stable biological, teaching, geometry, and scenario-selection
  contracts. Use temporary checks for numerical replay, runtime, and one-time full-pipeline proof.

## Milestones

Each milestone has one owner and must leave its evidence in the named implementation artifacts or
the progress record. Completion means the stated evidence has been inspected and accepted by the
manager.

| ID | Owner | Completion evidence |
| --- | --- | --- |
| M1. Save plan and comparison receipts | Documentation/evidence owner | This plan and its progress record are present; ordering and sorter receipts reproduce from the preserved experiment inputs; the manager accepts the recorded numbers and caveats. |
| M2. Integrate production repair and sorter | Implementation owner | Shared generation applies the workload-scoped repair before ordinary polish; accepted cases are ranked by the five-signal pool-relative score; review output reports the actual score and measures; cache remains score-free. |
| M3. Verify production behavior | Verification owner | Focused permanent tests protect meaningful contracts; temporary seeded checks cover ordering, 12% entry/stop behavior, rigorous workload scope, all three question forms, requested counts, mode and difficulty constraints, cache reuse, runtime, and full-suite status. Results and any failures are recorded. |
| M4. Document and close | Documentation owner with manager acceptance | Pipeline guide and changelog describe behavior, evidence, and limits; the completed local-search investigation is archived with valid links; temporary checks are classified and removed; the progress record contains accepted evidence for M1-M3 and all close-out links. |

## Completion rule

The plan remains active until M1-M4 each have accepted evidence. Marking the local-search
investigation complete does not complete this production consolidation. If an implementation
choice changes the settled behavior above, update this plan and progress record before treating
the affected milestone as complete.

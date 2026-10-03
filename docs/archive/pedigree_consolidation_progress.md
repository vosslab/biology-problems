# Pedigree consolidation progress

Plan: [pedigree_consolidation.md](pedigree_consolidation.md)

Status: complete. M1-M4 have accepted evidence. The earlier local-search investigation is archived
separately and did not substitute for these production milestones.

## Milestones

| ID | Status | Evidence |
| --- | --- | --- |
| M1 | Accepted by manager | The manager inspected and reproduced the ordering and sorter receipts. The sorter script joins all 1,000 cases, spatial measures, and bottom-empty measures one-to-one and reproduces the pooled top-quartile comparison on the frozen development/validation halves. The ordering replay reconstructs and checks all 100 preserved sources, then runs two matched replicates with fixed stage seeds and validates original people, states, parentage, teaching profile, and rigorous difficulty. |
| M2 | Accepted | The independent production replay passed on all 100 preserved rigorous sources, checking source immutability, parentage, inherited genotypes and phenotypes, teaching profile, evaluation, difficulty bounds, target, and stop conditions. Thirty-four changed; 20 ended at or below 0.12; 10 began at target and returned unchanged. Terminal conditions were the 26-person ceiling (55), no eligible geometry improvement (33), or one rejected sampled proposal (2). Easy, rigorous matching, and bonus repair calls were identity no-ops. |
| M3 | Accepted | All three rigorous commands produced two questions from fresh pools and score-free caches. Selection and matching retained all five modes under a shared generation/founder key. Fresh preparation took 2.69 s for identification, 12.46 s for selection, and 3.47 s for matching; cache reuse took 0.22 s, 1.14 s, and 0.38 s, loading 40/200/200 records without generation. Easy and bonus one-question checks passed (3 generations/14 people; 6 generations/76 people). The representative SVG was readable. Full suite: 4,888 passed, two existing line-limit warnings, 14.48 s; final focused metric/tie checks: 10 passed. No plan-specific files were present in `tests/_temp/`. |
| M4 | Accepted | Usage, changelog, and pipeline guide describe the production stages, evidence, and limits. The completed local-search plan and progress record are archived by `git mv`. The guide distinguishes the three new permanent contracts (content-based bottom-gap geometry, single rejected repair sample preserving the original, and stable ranking ties without input mutation) from one-time seeded replays. The final focused checks passed, links resolve, and the manager accepted M1-M3. |

## M1 receipts

- Sorter comparison: `../pedigree-aesthetics/consolidation/compare_sorters.py` and
  `../pedigree-aesthetics/consolidation/sorter_comparison.json`. On the development half, top
  quartile overall was 3.888 for equal-five versus 3.824 for the old score. On validation it was
  3.928 versus 3.888. Mode-balanced comparisons select each mode's top quartile by the same
  within-split global scores; they do not recompute component ranks within mode. Overall means
  were 3.781 versus 3.728 on development and 3.851 versus 3.845 on validation. The comparison is
  retrospective on an already selected top-1,000 corpus.
- Ordering comparison: `../pedigree-aesthetics/consolidation/replay_ordering.py` and
  `../pedigree-aesthetics/consolidation/ordering_comparison.json`. The two orders changed
  111/200 runs each. Repair then ordinary polish reached E <= 0.12 in 40/200 runs and had mean
  final E 0.184997; ordinary polish then repair reached it in 34/200 and had mean final E
  0.189106. Rounded to six decimal places, repair-then-polish had 19 paired wins, 5 losses, and
  176 ties. The comparison is geometric and invariant-based; it adds no blind ratings.
- Historical repair experiment and blind review: `../pedigree-aesthetics/downward_repair/REPORT.md`.
- Previous 1,000-case spatial analysis: `../pedigree-aesthetics/top1000/spatial/REPORT.md`.

## Close-out notes

The production target is 12% for both repair entry and stopping. Repair applies by the shared
rigorous workload definition: five generations and 23-26 people. The selected operation order is
downward repair followed by the existing bounded polisher. The sorter gives equal weight to five
pool-relative favorable percentiles. These are settled inputs to implementation; no additional
metric calibration is scheduled.

The 22.58% cutoff in the historical blind pilot is distinct from the production 12% geometry
trigger and target. The 12% target has not had a new blind review. The sorter comparison is
retrospective; pooled top-quartile overall ratings rose by 0.064 in development and 0.040 in
validation, while readability was slightly lower. Mode-balanced gains were smaller and mixed.
No calibration or new blind-rating campaign is part of this close-out.

The independent verifier's full command log, replay artifacts, runtime details, and results are
recorded in the sibling `pedigree-aesthetics/consolidation/verification/verification.md`.

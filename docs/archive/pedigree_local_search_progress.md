# Pedigree Local Search Progress

Plan: [pedigree_local_search.md](pedigree_local_search.md)

Status: complete. M1-M5 and WP1-WP8 have accepted evidence. Companion closeout records are synchronized to the final report hash. The plan remains the source of truth for scope and acceptance criteria.

## Milestones

| ID | Milestone | Status | Evidence / notes |
| --- | --- | --- | --- |
| M1 | Freeze evidence and inputs | Completed | `source source_me.sh && python3 ../pedigree-aesthetics/local_search/prepare_inputs.py` completed the freeze. All 1,000 actual original genotypes validated with 0 failures. The frozen set contains 100 selected cases (20 pilot, 80 confirmation; 10 per mode/band, split 2/8), 60 references plus 20 repeat references, and 23 source snapshots. Independent read-only protocol audit confirmed counts, source-genotype preservation, reference phases, hashes, and the corrected balanced review assignment. Plan saved and blind-review clarifications independently accepted; no plan-file changes since the M1 snapshot. |
| M2 | Implement and verify mutations | Completed | Independent final M2 review passed all three checks across all 100 frozen source cases. The structural removed-ID and direct-source-hash fixes are included; WP2-WP5 are complete. |
| M3 | Run the discovery pilot | Completed | All 20 pilot cases searched (47,627 proposals; run `9838866...`). Independent audits covered 1,795 checkpoint entries, 242 final candidate checks, run evidence, packet joins, and analysis. The blind-review set contains 251 ratings across 21 batches; these are not 251 independent cases. `PILOT_REPORT.md` and `confirmation_freeze.json` were accepted by the root manager with the existing design unchanged. The five-point rubric is coarse, and 20 independent starting cases limit precision; that is a pilot limitation, not a failure. No fitted weights or objective redefinition. |
| M4 | Run frozen confirmation | Completed | All 80 held-out cases completed under `confirmation_freeze.json` (189,519 proposals). Independent run audit validated 949 rebuilt final candidates and 7,120 checkpoint diagnostics. All 59 review batches and 536 ratings passed validation. Aggregate packet hash: `9d06eea893bd67543aeedad1d25a0b471bd71c5f5d8a1ec3c779d2dc0de1b9be`. The clipped-image sensitivity was resolved by independent inspection and rerating; original ratings remain preserved. |
| M5 | Analyze and recommend | Completed | Independent audit accepted exact-manifest statistics, biological diagnostics, sensitivity analysis, score crossings, plots, and the bounded yield/cost supplement. Pareto primary overall usefulness improved by +0.325 points (case-cluster 95% CI +0.200 to +0.450) across 80 cases. Fixed-cross p<0.05 diagnostics occurred in 18/80 Pareto outputs versus 2/80 originals; all recorded transmissions were valid. Under the descriptive reference-like benchmark, current and Pareto yields were 38/80 and 56/80; conditional linear extrapolation estimates 118 versus 80 starts for 56 such outputs. Recorded Pareto event time was 399.902 s; modeled break-even baseline cost is about 10.55 s/start, but baseline generation cost was not measured. Actual production savings and end-to-end break-even remain unknown. No production rollout is recommended. Final report SHA-256: `a0369e369aa4a3be63296aed0dcfb343dd05ecc5a0b1af9fc958045f734b42c8`. |

## Work packages

| ID | Work package | Status | Owner | Evidence / notes |
| --- | --- | --- | --- | --- |
| WP1 | Freeze inputs and protocol | Completed | Freeze agent | Ran `source source_me.sh && python3 ../pedigree-aesthetics/local_search/prepare_inputs.py`; all 1,000 actual original genotypes validated with 0 failures. Frozen set: 100 selected cases (20 pilot, 80 confirmation; 10 per mode/band, split 2/8), 60 references plus 20 repeat references, and 23 source snapshots. Independent read-only protocol audit verified counts, genotype preservation, reference phases, hashes, and the corrected balanced review assignment. Plan saved and blind-review clarifications independently accepted. |
| WP2 | Implement presentation edits | Accepted | `/root/presentation_ops_luna` | Independent audit accepted 100 cases, 1,886 recipes, and 337 presentation no-ops. Fingerprint recording is now implemented. |
| WP3 | Implement genetic edits | Accepted | `/root/genetic_ops_luna` | Accepted invariants: 84 sibling swaps, 64 terminal edits, and 709 branch edits. |
| WP4 | Implement structural edits | Accepted | `/root/structural_ops_luna` | Removed-ID fix completed; included in the independent final M2 review, which passed all three checks across 100 frozen source cases. |
| WP5 | Build evaluator and searches | Accepted | `/root/local_search_core_luna` | Direct-source-hash fix completed; included in the independent final M2 review, which passed all three checks across 100 frozen source cases. |
| WP6 | Prepare and review images | Completed | | Pilot and confirmation reviews are complete. Confirmation packet set `b0ef581c2c208a8f` contains 59 batches and 536 ratings; all batches and ratings are complete and validated. Aggregate packet hash: `9d06eea893bd67543aeedad1d25a0b471bd71c5f5d8a1ec3c779d2dc0de1b9be`. |
| WP7 | Analyze and audit evidence | Completed | | Pilot and final confirmation analyses, including the yield/cost/break-even supplement, passed independent audit. The estimate is conditional on the observed cohort and benchmark; actual production savings remain unknown. Evidence: sibling workspace artifacts `../pedigree-aesthetics/local_search/REPORT.md` and `../pedigree-aesthetics/local_search/runs/confirmation_analysis/analysis_confirmation_with_reviews.json`. |
| WP8 | Close documentation | Completed | | Final report, reproduction record, storage record, changelog entry, and completion matrix are present and accepted. Companion records are synchronized to final report hash `a0369e369aa4a3be63296aed0dcfb343dd05ecc5a0b1af9fc958045f734b42c8`. See sibling workspace files `../pedigree-aesthetics/local_search/REPORT.md`, `../pedigree-aesthetics/local_search/REPRODUCE.md`, `../pedigree-aesthetics/local_search/STORAGE.md`, and `../pedigree-aesthetics/local_search/COMPLETION_AUDIT.md`; repository record: [CHANGELOG.md](../CHANGELOG.md). |

## Final accepted evidence

The bounded yield/cost estimate is a cohort-conditional extrapolation using a descriptive
reference-like threshold; the baseline generation cost was not measured. It does not establish
actual production savings or an end-to-end break-even. Production ranking and polishing remain
unchanged. The full suite result is recorded in
Repository-root-relative log path: `../pedigree-aesthetics/local_search/verification/biology_problems_pytest_20261002.log`:
4,883 passed, 2 warnings, in 13.02 seconds.

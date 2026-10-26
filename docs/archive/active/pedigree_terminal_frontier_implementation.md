# Terminal-frontier implementation plan

## Status and authority

**Status: Complete.** Final policy, comparison, code review, fresh/cache smoke checks, and integration
review are complete. The implementation uses frontier construction for bonus identification only.

This file tracks implementation of the design hypothesis in
[pedigree_terminal_frontier_spec.md](../pedigree_terminal_frontier_spec.md). The specification
records the original proposal. This implementation plan records the settled decisions, approved
trial, and execution evidence; update it as implementation decisions or results change.

The goal is to make polished output depend less on later patching by constructing pedigrees whose
terminal generation already spans a useful horizontal frontier. This is a measured hypothesis,
not a guaranteed aesthetic outcome.

## Approved scope

- Extend child-slot planning to reserve source families and terminal sibships first, then build the
  middle generations that connect them.
- Enable the final trial for bonus identification only, using N=9 or N=10; easy remains on baseline.
- Leave medium, rigorous, matching, selection, and other formats unchanged during this trial.
- Keep family biology, rendering, and cache records designation-free. Designation is transient
  construction/analysis metadata.
- Separate topology construction, biological simulation, and displayed-layout validation. Check
  planned endpoints before biology and check them again against the actual `Diagram` after ordinary
  acceptance and any topology-changing stage.
- Retain current repair and polishing behavior during measurement. If either topology-changing
  stage breaks the endpoint contract, discard that stage's proposal and keep its accepted input.
- Keep the cache as the current eligible bank. No cache migration or CLI option is in scope.
- Do not turn an experimental quality metric into a permanent acceptance gate or remove polishing
  based on this trial alone.

## Implementation sequence

1. Add bounded source and terminal-family reservation to the child-slot planner. Preserve stable
   slot identity and reject impossible capacity or geometry through an explicit construction error.
2. Build connecting generations, allocate complete child tuples within current bounds, then create
   the family. Do not assume designated children are only children.
3. Keep `simulate_family` biological: founder alleles, transmission, and observations do not inspect
   designation. `questions.evaluate` handles acceptance separately.
4. Check a candidate's planned layout before biology. After biology and ordinary acceptance, check
   endpoint designation against the actual `Diagram`; reject candidates whose displayed deepest-row
   extremes are not designated or whose layout reports errors.
5. Wire only bonus identification scenarios to the new constructor, using N=9 or N=10. Preserve
   baseline construction for easy, all other difficulties, and other formats. Keep public
   `generate_candidate` on baseline construction; the actual-format pool path selects the trial.
6. Add focused permanent contract tests and run existing and full tests. Then collect the bounded
   comparison and blinded visual evidence below.
7. Treat the comparison as a moderate test of the design hypothesis, with readability and genuine
   pre-polish change as primary evidence. Polishing reduction is useful context, not the goal or a
   reason by itself to enable the trial. Record evidence and limitations before deciding policy.

## Contracts and interfaces

The initial shared API decision is:

- `sources.frontier_family(...)` constructs a family and carries IDs only as transient metadata. It
  raises `terminal_frontier.Rejected` for capacity or geometry rejection.
- `simulate_family(...)` handles biology without reading frontier metadata; `questions.evaluate`
  performs acceptance separately.
- `endpoints_match(...)` checks the rendered `Diagram`, after ordinary layout.

The pipeline helper is now settled:

- `scenarios._generate_candidate_with_receipt(mode, rng, level, matching=False,
  *, frontier_counts=())` returns `(AcceptedCase, tuple of IDs or None)`. Empty `frontier_counts`
  selects baseline behavior.
- Public `generate_candidate` keeps its legacy interface. `generate_pool(...,
  question_format=None)` selects frontier construction automatically only for actual identify
  output. Explicit match/boolean mismatches are rejected.

Keep the two pipeline scenarios and contract tests aligned to this interface. `Family`, renderer
inputs, and cache serialization remain free of frontier fields.

## Moderate evidence plan

Compare baseline and frontier constructors on 100 accepted targets: five inheritance modes, two
targeted difficulty levels, two constructors, and five seeded cases per cell. All 100 targets were
accepted. The 50 frontier candidates passed designated-endpoint checks; there were no endpoint
rollbacks. Easy median pre-polish `E` was 0.0861 baseline and 0.0923 frontier, with no polish
additions in either arm. Bonus median pre-polish `E` was 0.1373 baseline and 0.0138 frontier. Bonus
polishing added children in 8/25 baseline cases (13 additions) and 7/25 frontier cases (10
additions). This modest frequency difference does not establish reduced dependence on polishing.
Bonus median constructor-only time increased from 0.089 to 0.322 seconds; median total measured
target time, including instrumented stages, increased from 0.327 to 0.839 seconds. Median attempts
fell from 16 to 4, while maxima were 69 and 76. Median bonus family sizes were 78 and 86 people. Because the
within-preset family-size and terminal-family distributions differ, these measurements are
diagnostic and need visual interpretation. Full detail is in
[PEDIGREE_EVIDENCE.md](../../../problems/inheritance-problems/pedigrees/PEDIGREE_EVIDENCE.md) and the
provisional output directory `output_pedigree_frontier/comparison/`.

The blinded review preferred frontier construction in four of five bonus pairs; baseline was
preferred for X-linked dominant. Per-mode frontier readability ratings were 3, 3, 3, 3, and 4,
compared with 2, 3, 4, 3, and 3 for baseline. These ordinal judgments came from one reviewer and 10
pairs. Do not run a larger study in this stage. The sample is not statistical proof of a universal
improvement.

Focused durable tests cover stable topology, endpoint, rejection, simulation-separation, and
pipeline-routing contracts. After D8, all 13 terminal-frontier tests, all 148 pedigree tests, and
the full 5,035-test repository suite pass. The full suite reports two existing source-length
warnings for `bptools_legacy.py` and `webwork_lib.py`; scoped pyflakes also passes. Four real identify
CLI runs cover easy and bonus with fresh and cache-backed generation: each generated 20 candidates
freshly and 20 from cache. The output audit found 14 directories, 42 BBQ/HTML/ZIP artifacts, and 34
valid SVGs. The receipt at `output_pedigree_frontier/smoke/SMOKE_REPORT.md` separates the initial
14-format matrix, which predates D8, from the final four easy/bonus identify runs. A browser
screenshot launch failed in the sandbox; generated artifacts were inspected directly and comparison
PNGs were reviewed separately. Follow the repository directive to invoke Python with
`source source_me.sh && python3`.

The numerical results show no easy construction advantage and a strong bonus pre-polish `E`
reduction, with slower construction and larger median families in the bonus frontier arm. The 10-pair
review preferred frontier in four bonus comparisons, with one exception. Decision D8 enables the
frontier for bonus identification only, with random terminal counts 9 or 10; easy remains on
baseline. Keep polishing and all existing acceptance gates. This verdict does not establish student
benefit or a general visual-quality rule.

## Execution ledger

The implementation, evidence decisions, and final-policy validation are recorded below.

| Task | Owner | Status | Depends on / evidence |
| --- | --- | --- | --- |
| Sources and terminal-frontier layout construction | `construction_luna` | Implemented; reviewed | `terminal_frontier.py`, `sources.frontier_family`; independent review accepted |
| Scenario and difficulty pipeline | `pipeline_luna`, `final_policy_luna` | Implemented; D8 verified | Bonus identification only; baseline public candidate API |
| Contract tests | `contracts_luna`, `final_policy_luna` | Implemented; reviewed | 13 focused `test_terminal_frontier.py` tests pass; all 148 pedigree tests pass |
| Plan and focused documentation | `documentation_luna` | Complete; accepted | This file, four pedigree authorities, design decisions, and changelog updated |
| Comparison and visual review | `comparison_luna`, `visual_review_luna`, `visual_correction_luna` | Complete | 100/100 accepted; 50/50 frontier endpoints valid; review preferred frontier in 4/5 bonus pairs |
| Validation and code review | `root`, `spec_review_luna`, `quality_review_luna` | Complete; accepted | 5,035 tests pass; 2 existing source-size warnings; scoped pyflakes passes |
| Fresh/cache output smoke | `writer_smoke_luna`, `root` | Complete | Four identify CLI runs; 14 output directories; 42 BBQ/HTML/ZIP artifacts; 34 valid SVGs |
| Documentation links | `documentation_luna` | Complete | `source source_me.sh && pytest tests/test_markdown_links.py -q`: 80 passed |
| Temporary harness cleanup | `cleanup_luna` | Complete | Temporary scripts and bytecode removed; output evidence preserved |
| Final integration review | `integration_review_luna` | Complete | Accepted; no blocking findings |

### Decisions

| ID | Decision | State |
| --- | --- | --- |
| D1 | Transient topology metadata; biology-only simulation; actual layout endpoint checks and rollback after topology-changing stages | Implemented; accepted review |
| D2 | Moderate evidence: 5 modes x 2 levels x 2 constructors x 5 seeds, plus 10 blinded pairs | Complete; limitations recorded |
| D3 | Test the construction hypothesis with correctness, pre-polish change, retries, and readability; treat polishing reduction as context | Applied in D8 |
| D4 | Keep planned terminal sibling order stable; preserve existing procedural shuffle behavior | Implemented; accepted review |
| D5 | Keep frontier IDs transient and out of biology, renderer inputs, and cache records | Implemented; accepted review |
| D6 | Do not run Git or staging operations; no rename is required | Settled |
| D7 | This implementation plan is the settled execution record; the original spec records the proposal. Simulation performs biology only, while geometry and endpoint checks run before biology and after layout acceptance. | Wording correction applied; spec and quality reviews accepted |
| D8 | Enable frontier construction only for bonus identification, with random terminal counts 9 or 10; keep easy and all other paths on baseline. Retain polishing and current acceptance gates. | Implemented; final verification complete |

### Coordination notes

- Preserve existing user changes; do not perform Git index operations.
- Invite questions when implementation exposes a material ambiguity. A clarified decision remains
  open until affected owners restate it, apply it, and verify the result.
- The representative six-generation, N=9 bonus contract is covered by a durable test. Review and
  cleanup are complete; generated comparison and smoke evidence remain under `output_*` paths.

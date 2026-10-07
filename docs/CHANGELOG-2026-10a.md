## 2026-10-05

### Behavior or Interface Changes

- Added terminal-frontier family construction for bonus identification pools. The
  constructor reserves terminal sibling slots before connecting middle generations; transient
  designated IDs remain outside family biology, renderer inputs, and cache records. The pipeline
  validates geometry before simulation and checks the rendered endpoints after acceptance and
  topology-changing stages, rolling back a proposal that breaks the endpoint contract.
- Recorded the 100-target and 10-pair moderate comparison. Bonus identification enables random
  frontier sizes 9 or 10; easy and all other paths keep baseline construction. Polishing remains
  unchanged and its small frequency difference is not treated as a benefit.

### Developer Tests and Notes

- Final validation passed 13 terminal-frontier tests, all 148 pedigree tests, and the full suite
  (5,035 passed; two existing source-length warnings). Four fresh/cache identify CLI runs passed;
  42 BBQ/HTML/ZIP artifacts and 34 SVGs were audited. All 80 Markdown-link checks passed. The
  100-target comparison accepted every target; one reviewer preferred frontier in four of five
  bonus pairs. See [PEDIGREE_EVIDENCE.md](../problems/inheritance-problems/pedigrees/PEDIGREE_EVIDENCE.md).

## 2026-10-04

### Behavior or Interface Changes

- Refined both plant-question layouts: regular reference tables sit beside each other
  when space allows and stack on narrow screens. Whole two-gene genotypes stay together,
  allele text matches the surrounding font size, and bonus crosses occupy separate lines.
  Shortened setup wording and brightness-table labels. Bonus questions now ask for the
  probability of an offspring's phenotype after random selection of the first-cross plant.
- Corrected doubled table-image display sizes in the companion `qti-package-maker`
  exporter so the compact layout also survives Blackboard image conversion.
- Revised the two plant probability generators against the new question voice and pedagogy
  guides. Genotype tables come first, parents' colors and markings occupy separate columns,
  and specific target combinations use labeled fields instead of nested phenotype phrases.
  Removed repeated table explanations and shortened probability lead-ins. Numbered allele
  subscripts and italic letters are retained with monospace formatting.
- Replaced arbitrary fraction substitutions with named genetic errors: omitted genes,
  complete-dominance assumptions, missed heterozygote routes, wrong genotype rows, memorized
  parental crosses, and incorrect conditioning in the bonus questions. Worked choices sort
  by probability and use distinct results. Some regular scenarios have three meaningful
  choices instead of padding to four. Pools still contain 378 regular and 144 bonus scenarios.
- The bonus brightness table now runs from dark for no glow to light for very high brightness,
  with readable foreground colors and text labels. Cross wording avoids "a A1A2 plant".

### Developer Tests and Notes

- Layout follow-up: checked five items per generator at 900- and 375-pixel widths in both
  native HTML and actual packaged Blackboard HTML with resolved images. Verified all 522
  keys independently; the 35 focused biology tests and 23 companion image-export tests
  passed. Current gallery, matching before/after examples, screenshots, and export checks
  are under `output_plant_voice/layout/`. No live Blackboard import was performed.
- All 522 keys matched an independent enumeration of physical gamete pairs, including
  phenotype selection and the second cross. Every displayed calculation was verified;
  wrong choices map to named errors and choices remain in numerical order. The focused plant
  and bptools suite passed 35 checks. Scoped pyflakes and diff whitespace checks passed.
- Reviewed five rendered items per generator and before/after samples in
  `output_plant_voice/`. The advisory checker went from 144 article findings in the bonus
  stems to no findings in either complete pool. Both layouts fit a 375-pixel viewport.
  Five fresh CLI items per generator exported to self-test HTML and Blackboard ZIPs with
  valid XML and 15 regular/5 bonus table PNGs. Exported tables were visually inspected;
  brightness text contrast ranges from 4.93:1 to 14.27:1.
  `output_plant_voice/REVIEW.md` records the authoring contract, rubric review, distractor
  rationales, and key-verification evidence. No full repository suite or live LMS import ran.

## 2026-10-03

### Additions and New Features

- Added canonical guidance for student-facing question text:
  [QUESTION_PEDAGOGY_GUIDE.md](QUESTION_PEDAGOGY_GUIDE.md) (puzzle-first design workflow,
  error-derived distractors, seriously absurd choices, item structure, statement and matching
  banks, answer verification, a review rubric routed by item type, and verified references),
  [QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md) (stem anatomy, emphasis, hints, choice layout
  and ladders, per-type instructions, numbers, formatting, mechanics), and
  [QUESTION_EXEMPLARS.md](QUESTION_EXEMPLARS.md) (verbatim model and fix examples from Neil's
  exams, pre-agent generators, and banks, each citing its rule).
- Added [QUESTION_EVIDENCE.md](QUESTION_EVIDENCE.md): the corpus audit behind the guides (exam,
  generator, and bank quotes; Neil's 2026 correction log; defects found) plus verified published
  research (Haladyna 2002, NBME guide, Rodriguez 2005, humor-in-testing studies, LLM item-quality
  studies) and local book passages with search terms. Bundled into both writer skills.
- Added `devel/check_question_text.py`, an advisory checker that reads BBQ files and reports
  testwiseness cues and text slips: longest key (K1), hedge/absolute asymmetry (K2), key-word
  echo (K3), article slips (K4), spacing (K5), stem/choice unit mismatch (K6), and generic
  lead-ins (K7). It always exits 0 and strips hidden anti-cheat spans before checking.

### Behavior or Interface Changes

- Rewrote the example content of `problems/TEMPLATE.py` as a small dilution puzzle: data-first
  stem, randomized scenarios, distractors each computed from a named student error (commented),
  one optional deadpan absurd choice, and natural ascending choice order. Structure, argparse,
  and `main()` are unchanged; the old example kept two correct-looking terms in its choice pool.
- [QUESTION_AUTHORING_GUIDE.md](QUESTION_AUTHORING_GUIDE.md) gains a "Student-facing text"
  section and an error-derived skeleton example; the assert advice now points to `tests/`.
- The MC-statement and matching-set authoring guides now link to the canonical guides for
  wording and pedagogy rules (larger false pools, one-term swaps, balanced hedges, absurd choices,
  values without key-word echo) instead of restating or contradicting them.
- `AGENTS.md` points student-facing text work to the three guides.

### Fixes and Maintenance

- Recorded the decision that question-writing guides are canonical here and bundled into the
  `bptools-writer-expert` and `webwork-writer-expert` skills
  ([DESIGN_DECISIONS.md](DESIGN_DECISIONS.md)), and five of Neil's statements on question writing
  in [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md).
- The template now samples a richer pool of named-error dilution choices before natural sorting,
  so a fixed error-choice prefix does not reveal the requested answer position.

### Decisions and Failures

- The writer skill had no guidance on student-facing text and demanded a `--seed`
  byte-identical proof that `bptools.py` cannot produce; agent effort went to infrastructure
  proof instead of reading the questions. The new guides and the skill's review step address this.
- Neil loves seriously absurd choices; published guidelines count blatantly absurd options as a
  giveaway. Resolution: absurd choices are welcome, and authors judge whether the remaining
  alternatives assess the intended reasoning. The guides set no numeric quota for either kind.
- Found during the audit and left for separate follow-up: `x_linked_tortoiseshell.py` keys every
  "daughters" question "None, 0%" (it compares "daughters" to the sex label "female"), and
  `serial_dilution_factor_mc.py` states a total in uL with choices in mL.
- `QUESTION_EVIDENCE.md` is the durable audit and evidence record, replacing the plan's proposed
  duplicate `docs/active_plans/audits/question_voice_audit.md`.
- The initial literal blind replay tied both arms at 189/200 rubric-category points. The accepted
  loop-one revision narrows general guide language on scenario variety, misconception pairs, and
  ratio order without numerical quotas or forced no-replacement; affected treatment arms will be
  rerun before any improvement claim.
- The initial literal replay tie at 189/200 remains valid. A first loop-one set-level summary
  (41/44) and provisional 95%/92.5% comparison were corrected before review. Independent final
  review accepted the corrected loop-one sample: control 185/200 (92.5%) and treatment 192/200
  (96.0%) across R1 60/60 versus 52/60, R2 60/70 versus 70/70, and R3 65/70 versus 70/70. No
  second guide loop is required.

### Developer Tests and Notes

- Added `tests/test_check_question_text.py` (hidden-span stripping, longest-key margin, hedge
  asymmetry, article slips including "an X-linked", missing spaces). The pre-integration full
  suite passed 4,989 tests; the final full suite passed 4,993 tests with two pre-existing
  source-size advisory warnings (`bptools_legacy.py` and `webwork_lib.py`).
- A one-time exhaustive template verifier covered 32 dilution scenarios with 2, 3, 4, and 5
  choices, confirming unique naturally ordered choices and varied answer positions. It was then
  removed rather than promoted to a permanent test.
- During the in-progress blind evaluation, all 60 independently checked replay answer keys are
  correct. The WebWork incomplete-dominance item now passes lint, accepts `0.5`, rejects `0.25`,
  and passed screenshot review; the initially bare description and answer-revealing entry example
  remain recorded in the evaluation evidence. Final scoring and review remain pending.
- Across both evaluation rounds, all 120 independently checked answer keys are correct; V4 runtime
  and V5 dry-run checks are complete. The corrected final comparison passed independent review.
- An independent review agent checked the guides for duplicated rules, citation and anchor
  resolution, positive phrasing, example correctness, and coverage of Neil's 2026 corrections;
  its findings (including a misattributed quote and a wrong explanation of a gene-map item) were
  fixed. 85 "guide > heading" citations resolve.

## 2026-10-02

### Changed

- Integrate rigorous-workload bottom-gap repair before the existing bounded pedigree polisher,
  followed by five-signal equal-mean percentile ranking and normal scenario assembly. The repair
  uses 12% as both its geometric entry trigger and stopping target, preserves original people,
  and respects the current five-generation and 26-person limits. Existing 24-hour cache expiry
  remains unchanged; cached cases are revalidated and ranked against the current pool without
  biological repolishing. Scores are pool-relative, not calibrated quality estimates.
- Replace the pedigree pipeline guide's old ranking formula and removal instructions with the
  current repair, polishing, sorting, cache, and module contracts.
- Split the pedigree reference into focused workflow, difficulty, biology, layout, polishing,
  ranking, probability, and graph-analysis authorities; correct the bonus and generation-specific
  construction bounds against the current preset tables. Start at
  [PEDIGREE_PIPELINE.md](../problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md) for the
  full document map.

### Investigated

- Retrospective comparison of the equal-five sorter on 1,000 reviewed top-pool pedigrees found
  top-quartile overall means of 3.888 vs 3.824 in development and 3.928 vs 3.888 in validation.
  Mode-balanced gains were smaller (3.781 vs 3.728; 3.851 vs 3.845), and readability was slightly
  lower in both pooled splits. The 22.58% blind pilot cutoff remains historical and differs from
  the production 12% geometric target; the 12% target has no new blind review. No new calibration
  is planned. Evidence and reproduction receipts remain in sibling `pedigree-aesthetics`.

### Added

- Add `-A` / `--autosomal` to all three pedigree writers for autosomal dominant/recessive warm-ups.
  Restrict fresh and cached pools, answer choices, and comparable sets to those two modes; add an
  `autosomal` export suffix so warm-up sets can coexist with the full five-pattern sets.

- Preserve the fixed pedigree visual-review rubric and accumulated evidence in repository-owned
  [PEDIGREE_RUBRIC.md](../problems/inheritance-problems/pedigrees/PEDIGREE_RUBRIC.md) and
  [PEDIGREE_EVIDENCE.md](../problems/inheritance-problems/pedigrees/PEDIGREE_EVIDENCE.md). Record the
  distinction between hard biology/teaching gates and aesthetic ratings, corrected local-search
  pilot values, empirical limits, and rationale for the current 12% repair target and equal-five
  sorter. Detailed case data remain in the sibling research checkout.

- Add a diagnostic-only offspring probability tool using original parental genotypes,
  all five inheritance modes, and equal offspring sex probability. Report sex-by-phenotype
  Pearson statistics, Monte Carlo fixed-cross tail probabilities, the worst unadjusted
  sibship p-value, and impossible transmissions. Keep ranking and acceptance unchanged.
  CLI: `tools/pedigree_probability.py`; definitions and input format are in
  `problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md`.
- Preserve a one-time paired 1,000-pedigree rigorous comparison in sibling
  `pedigree-aesthetics/offspring_probability/`. Before/after polishing, p < 0.05 occurred
  in 31/33 cases and p < 0.01 in 9/9; no impossible transmissions. This is a fixed-cross
  diagnostic, not proof of unbiased generation. Retain focused probability-contract tests;
  repository suite: 4,850 passed.

### Changed

- Let bounded pedigree polishing choose the best structural terminal-child placement before
  drawing a single weighted Mendelian genotype. Preserve the two-child budget and acceptance
  gates; do not choose or reroll phenotypes to improve affected distribution. Compare teaching
  profile presence rather than diagnostic affected-sex counts, fixing the old rule that rejected
  every affected addition. Preserve the existing whole-pedigree ranking formula.
- Compare old and revised polishing on the same 200 ordinary rigorous pedigrees in sibling
  `pedigree-aesthetics/local_polisher/`. Mean ranking score improved by 0.071 over old polishing;
  affected-region coverage rose by 0.010. These are heuristic measurements, not new Luna ratings.
  Old polishing added 161 unaffected children and no affected children; the revised version
  added 137 children including 34 affected, versus a cross-specific expectation of 33.5 among
  those accepted additions. Acceptance still conditions the sample. Retain one regression for
  keeping either sampled outcome at the same placement; keep corpus checks experimental.

### Investigated

- Evaluated bounded downward growth on 100 fresh accepted rigorous pedigrees in sibling
  `pedigree-aesthetics/downward_repair/`. Geometry-first repair adds a valid child in the
  largest bottom-anchored empty rectangle when E exceeds the frozen historical Q3 cutoff
  (0.22578), stopping at or below the cutoff, when no improving legal placement exists, after
  the first sampled candidate fails an acceptance gate, or at the 26-person ceiling. Thirteen
  cases changed; mean empty-space fraction fell by 0.009 across
  all cases and 0.068 among changed cases. Blind ratings improved overall usefulness by 0.09
  and balance by 0.08 across all 100 cases; changed cases improved by 0.69 and 0.62,
  respectively. Crop-claim sensitivity retained a +0.08 overall change. Five changed cases
  remained above cutoff at the size ceiling. Fixed-cross p < 0.05 counts were 3/100 before and
  after; retained outcomes remain conditioned on biological, teaching, difficulty, and layout
  gates. This small feasibility study does not validate the cutoff or establish production
  yield or unbiased outcomes; production behavior remains unchanged. Full suite: 4,883 passed.

- Complete frozen confirmation and blinded ratings for the local pedigree-search experiment in
  sibling `pedigree-aesthetics/local_search/`. Across 80 held-out cases and 536 ratings, Pareto
  primary selection improved overall usefulness by +0.325 points (case-cluster 95% CI +0.20 to
  +0.45); scalar selection improved it by +0.025 while readability changed by -0.25. Fixed-cross
  probability diagnostics were below 0.05 for 18/80 Pareto-selected pedigrees and 2/80 originals,
  consistent with selection enriching candidates with low fixed-cross p-values; every recorded
  transmission was valid. The accepted report and independent analysis audit support experimental
  findings only. A supplemental cohort-yield calculation estimates 32.1% fewer starts for the
  same 56 benchmark-yield cases, with a 10.55-second baseline-cost break-even under equal-cost and
  linear-yield assumptions; actual production savings remain unknown. Production ranking and
  polisher behavior remain unchanged. Reproduction commands, input hashes, and measured artifact
  storage are recorded in sibling
  `pedigree-aesthetics/local_search/REPRODUCE.md` and `STORAGE.md`.
- Explored lower-row empty space as an image measure in sibling
  `pedigree-aesthetics/bottom_empty_space/`. Empty fraction correlated with balance in both
  historical halves (rho -0.320/-0.286), and weakly with overall rating (-0.152/-0.141) and
  interest (-0.067/-0.094). Across 80 paired Pareto outputs, mean empty fraction fell by 0.073;
  its change correlated with changes in overall rating (-0.342) and balance (-0.400). These are
  experimental associations; production ranking and acceptance remain unchanged.

## 2026-10-01

### Investigated

- Reused the 1,000 rigorous Luna ratings for spatial measurements; preserved the follow-up
  in sibling `pedigree-aesthetics/top1000/spatial/REPORT.md`. Affected quadrant coverage
  correlated with interest at +0.322/+0.304 across the existing halves; affected generation
  coverage at +0.363/+0.380. General area fill was weaker. Retired diameter/radius as ranking
  candidates; neither was in production ranking. Production weights remain unchanged.
  Also tested occupied-cell affected coverage at the user's two native cell sizes:
  2 generations x 4 sibling pitches gave interest +0.343/+0.347; 3 x 5 gave +0.308/+0.283.
  Preserved boundary sensitivity and confounding caveats; no difficulty-specific grid added.

- Reviewed the highest-ranked 1,000 final images from 10,000 valid, polished,
  five-generation rigorous pedigrees with the fixed blind Luna-6 rubric, split into 500
  development and 500 validation cases. Preserve all scored candidates and the analysis in
  sibling `pedigree-aesthetics/top1000/analysis/REPORT.md` and `scored_cases.json`.
  Outside affected-reach fraction again correlated negatively with interest (rho -0.30
  development, -0.29 validation). Top-100 overall ratings exceeded the next 900 (3.940 vs.
  3.684), but selected-only reviews cannot establish improvement over a random valid pool.

- Measured affected ancestry reach and trailing unaffected generations on the existing 200
  polished pedigree reviews. Preserved the script, annotated gallery, raw measurements, and
  limitations in sibling `pedigree-aesthetics/AFFECTED_REACH.md`. Unaffected relatives can
  supply teaching evidence; production ranking and acceptance rules remain unchanged.

### Changed

- Make HTML pedigree widths follow the question font size instead of a pixel width capped
  at 75% of the container. Wide drawings scroll in a keyboard-focusable region, so zoom
  enlarges symbols and labels without shrinking them back to fit. Preserve the 2 px stroke
  floor. Existing website questions must be regenerated to receive the new markup.

- Add outside affected-reach fraction to pedigree ranking with a modest 0.1 penalty weight:
  `progression - mean_row_density - 0.1 * outside_fraction`. Isolate the visible-ancestry
  measurement from ranking and acceptance. Preserve unaffected ancestors and immediate
  partners; do not prune or reject people outside reach. The existing affected-depth gate
  remains separate. Retain one measurement-contract test without pinning the tunable weight.
  Production measurements match all 200 archived cases; full suite: 4,843 passed.

- Keep pedigree connectors, symbol outlines, and the HTML frame at fixed 2 px (1.5 pt),
  above the requested 1 pt minimum during 75% and responsive scaling. SVG strokes no longer
  scale; browser checks at 320, 600, and 1200 px confirmed the HTML stroke floor.
- Require a visibly affected individual in either of the last two pedigree generations through
  the shared teaching acceptance gate, including cached cases and polished candidates. All
  five modes remain generatable across every supported difficulty/matching preset (70 fresh
  polished cases checked). Retain one parametrized acceptance-boundary regression; browser
  measurements and the preset sweep are one-time checks. Full suite: 4,833 passed.

- Reduced pedigree display width and height by 25% in HTML questions and SVG review
  exports, preserving family sizes, layout geometry, and proportions.

- Enlarged bonus pedigrees to 6-7 generations and 60-100 individuals, with 3-4 founding
  couples and 18-26 total couples. Existing smaller bonus cache records are ineligible.

- Split the pedigree bank into `pedigree_cache_easy.jsonl`, `pedigree_cache_medium.jsonl`,
  `pedigree_cache_rigorous.jsonl`, and `pedigree_cache_bonus.jsonl`. Each file expires
  independently after 24 hours without an append. Records omit the difficulty supplied by
  the filename, and runs load only their requested difficulty.

- Continue drawing eligible cached pedigrees when the first sample cannot form enough
  comparable selection or matching sets, generating fresh candidates only after exhausting
  the eligible bank. Centralized compact record identity for duplicate detection and storage.

- Delete and recreate the pedigree JSONL bank on the next run after 24 hours without an actual
  append. Fresh generation appends within the current window; stale banks are replaced even
  with `--fresh`. A separate lock file coordinates expiry with readers and writers. Reads and
  duplicate-only appends do not refresh the expiry clock.

- Added an ignored compact JSONL pedigree bank shared by all three generators. Default runs
  and `--use-cache` reuse eligible records and generate shortages up to the `-d` candidate target;
  `--fresh` bypasses reads and appends new accepted pedigrees. Difficulty and matching limits
  are checked separately; carriers stay hidden, biology and layouts are revalidated, records
  remain reusable across runs, and file locks protect concurrent appenders. Storage uses only
  level, mode, sex, affected/carrier indices, and parent/child connections.

- Cached pedigree family member indexes, parentage, and validated generation ranks per
  immutable family. Public methods still return independent dictionaries, and replaced families
  validate their own structure. Three seeded 200-candidate easy identification runs retained
  identical results; median preparation time fell from 3.21 to 2.59 seconds locally (19%).

- Made pedigree candidate-pool sizing depend on `-d` alone; `-x` still caps exported
  questions but no longer reduces the preparation pool.

- Included the selected difficulty (`easy`, `medium`, `rigorous`, or `bonus`) in output
  filenames for all three pedigree generators, including derived Blackboard and self-test exports.

- Hid `--hidden-terms` and `--noclick-div` from shared bptools CLI help while keeping
  both options available with their existing defaults and behavior.

- Hid development-only pedigree `--seed` and `--review-dir` options from normal CLI help;
  both options and their short aliases remain available for verification and review exports.

- Added single-letter aliases to all three pedigree question commands: `-E` for `--easy`,
  `-M` for `--medium`, `-R` for `--rigorous`, `-b` for `--bonus`, and `-C` for
  `--random-color`. Bonus remains limited to pedigree identification.

- Enforced the rare-trait rule across pedigree generation and homework assessment:
  generation-I individuals and inherited descendants may be carriers, but unrelated spouses
  entering in generation II or later cannot be unaffected carriers. Affected spouses remain
  allowed. Autosomal recessive later spouses are sampled as 90% homozygous unaffected and
  10% affected; these are teaching weights, not population frequencies. Polishing reuses the
  acceptance gate. Kept unrestricted Mendelian analysis as the library default, with optional
  noncarrier constraints for homework, and added the rare-trait assumption to question text.
  Revised the bundled recessive example so later spouses no longer require carrier status.
  Retained focused permanent tests of the carrier contract; generation/polishing sampling,
  preset exports, timings, seeded byte comparison, and visual checks were one-time evidence.

- Added `--affected-color` and `--random-color` to all pedigree generators. Random color
  selects one of 14 dark hues per question, consistently across all its diagrams and SVG
  review exports, with seed reproducibility. Black remains the default. Darkened the supplied
  palette to at least 9:1 contrast against white; unfilled symbols remain white.

- Removed the symbol legend from all three pedigree question formats; students must
  know or look up the conventions. Retained the complete-penetrance and no-new-mutations
  assumptions in the question text.

- Added a thin gray frame around each HTML pedigree, including the drawing table
  used for image exports, to separate diagrams visually in answer choices.

- Made easy difficulty the default for all three pedigree generators; explicit
  `--medium`, `--rigorous`, and supported `--bonus` selections remain available.

- Scaled the shared pedigree candidate pool to 20 times the required pedigree count
  (respecting `-d` and `-x`) instead of always polishing 5,000 candidates. Selection and
  matching multiply by five for their five pedigrees per question. The preparation message
  reports the actual pool size; default runs use 40 candidates for identification or 200
  for selection and matching.
  The CLI reports elapsed preparation time, including generation, polishing, and assembly.
  Small pools lacking complete comparable sets receive additional batches of the same size,
  capped at ten batches, with progress reported for each addition.

- Renamed `hypothesis_statements.py` to `null_and_alternative_hypotheses.py`
  and `hypothesis_lab_partner.py` to `hypothesis_statement_errors.py` to describe
  their learning objectives. Updated documentation, classifier inventory, and
  website task inputs; generator content and options are unchanged.

- Renamed three biostatistics YAML banks to describe their learning objectives:
  `selecting_statistical_tests.yml`, `hypothesis_testing_terms.yml`, and
  `hypothesis_testing_decisions.yml`. Updated bank index, classifier references,
  and website task inputs; question content is unchanged.

- Matched the babies two-sample t-test and population-test question headings to
  the one-sample t-test: Setup, Sample data, Procedure, and Result to report.
  Renamed `population_test_google_sheet.py` to `babies_one_sample_z_test.py` to
  match the babies test naming pattern and its default z-test; retained its optional
  t-test mode and updated repository references.
- Added a dedicated one-sample babies versus national average t-test generator,
  linked to the Part 2 Google Sheets tutorial. Its question is organized as setup,
  sample data, procedure, and result to report. It uses the sample standard deviation,
  asks for the tutorial's p-value cell, supports greater-than and two-tailed p-values,
  and accepts a seed for repeatable banks.
- Integrated bounded pedigree polishing and a deterministic interestingness sort into all
  three generators: valid candidate, at most two checked terminal-child additions, difficulty
  filtering, progression-first ranking with lower mean row density breaking ties, then normal
  scenario assembly. Isolated measurements, polishing, and scoring for later revision; retained
  experiment artifacts as rationale without production dependencies or further calibration.
  Excluded impossible depth/founder choices from generation using the constructor's minimum
  union count, fixing rigorous four-generation matching with the existing five-couple cap.
  Retargeted archived changelog links to the renamed pedigree commands while retaining
  their historical labels. Reviewed tests against the permanent-test checklist: removed
  aesthetic-formula and arithmetic checks, retained family/evidence preservation contracts.
  The full 4,743-test suite passes; all three full-pool generators emitted the requested counts.
- Generated a fresh 200-case development corpus with polishing applied to every case
  and blind Luna-6 ratings under the unchanged rubric. Preserved all raw measurements
  and analyzed the new population separately from historical reviews. Progression and
  row structure showed repeatable weak signals; no new production score was integrated.
>>>>>>> b5b5cf7 (Integrated bounded pedigree polishing and a deterministic i... (+1 more))
- Investigated terminal-child pedigree polishing in the sibling experiment directory.
  On 200 larger MC cases, bounded additions reduced shrinkage in 127 while preserving
  existing inheritance evidence, difficulty, and layout checks. Production is unchanged.
  Two independent final-image-only reviews rated the ten-example gallery 3.8 and 4.4
  overall out of five; this does not measure improvement over the original diagrams.
  The experiment also exposed an infeasible rigorous matching preset combination:
  four generations and three founding couples cannot fit the five-couple cap.
- Allowed three or four generations for rigorous pedigree matching, retaining its smaller
  16-18-person workload. Rigorous MC remains exactly five generations. Created a fresh
  development gallery of 20 nonnegative-progression MC pedigrees and 20 matched negative
  controls in the sibling experiment directory; production progression filtering is unchanged.
- Applied the permanent-test checklist to `test_inheritance_scenario_pools.py`.
  Retained unique question stems, single answer membership, and finite-pool exhaustion;
  removed one-time organism/icon integration and capacity-cap wiring checks that pinned
  internal representations and diagnostic wording.
- Renamed the three pedigree generators by direction: `write_pedigree_to_pattern.py`,
  `write_pattern_to_pedigree.py`, and `write_pedigree_pattern_matching.py`. Removed the
  legacy matching wrapper and retired prebuilt-bank generation and its source/YAML flags.
  All three use random ranked pools; authored examples remain library fixtures only.
- Integrated the fixed people-per-width pedigree ranking into all three homework commands.
  Prepare 5,000 valid candidates, retain existing difficulty and acceptance checks, assemble
  comparable five-mode sets where required, and consume scenarios through bptools with
  randomized question and choice order. Keep geometry, scoring, and pool assembly in small
  separate modules. Closed aesthetic calibration without adding score terms; preserve its
  mixed results and galleries in the sibling `pedigree-aesthetics` experiment directory.
- Merged the fly and yeast lethal-allele sets into `lethal_allele_survival.py`.
  Shuffle one combined scenario pool so each question uses a randomly selected
  organism with its matching phenotype dictionary and icon. Removed the separate
  yeast wrapper; preserve percentage sorting, thirds emphasis, and shared genetics.
- Sorted lethal-allele fraction and calculation choices by increasing percentage,
  and ratio choices by increasing ratio. Include both 1/3 and 2/3 in fraction/count
  choices and weight scenarios with those correct probabilities eight times more
  heavily. Apply to both fly and yeast sets; retain random scenario ordering and
  varied remaining distractors while intentionally keeping choices in numeric order.
- Clarified the denominator in both lethal-allele question sets with "Before considering
  survival, assume the cross produces N offspring" and "How many would you expect."
  Retain separate wording for counts of surviving offspring and the existing
  calculation choices.
- Replaced fixed phenotype descriptions in `lethal_allele_survival.py` with two
  distinct positive labels from the shared hypothetical fly phenotype dictionary.
  Explicitly label the trait hypothetical and use the same names in the table, rule,
  and question. Randomly assign a genetic scenario to each of the 650 ordered phenotype
  pairs, then shuffle the pool; support 199 questions without repeated phenotype pairs.
  Added `lethal_allele_survival_yeast.py` as a parallel budding-yeast generator sharing
  the same genetics and presentation. Each version uses its dictionary's organism
  name and phenotype vocabulary, plus one ASCII-escaped fly or microorganism emoji
  at the start of the setup paragraph; retain probabilities and calculation choices.
- Simplified `lethal_allele_survival.py` to a compact genotype/outcome table, explicit
  dominance rule and lethal exception, labeled parent cross, offspring count, and direct
  question. Added a red X emoji beside the lethal outcome and monospace genotypes.
  Lethal questions now name the homozygous lethal genotype; retain calculation choices,
  randomized scenarios, and the distinction between all offspring and survivors.
- Introduced Parent 1 and Parent 2 explicitly in every monohybrid cross sentence
  and repeated Parent 1's known genotype in the conclusion question. Separate the
  full genetics setup from the experiment with a blank line that survives export;
  keep the experiment, result, and conclusion on consecutive lines. Restore plain
  "all have" observations when only one offspring phenotype is present.
- Added a genotype column beside each phenotype in the monohybrid observation
  table, using the same randomized allele letters as the full setup and choices.
  Retained the explicit genotype-to-phenotype setup sentence and restored numeric
  phenotypic ratios for every cross, including 1:0 and 0:1.
- Standardized every `monohybrid_litter_inference.py` prompt as four separate
  sentences: dominance/phenotype setup, the known-parent cross, observed results,
  and the genotype conclusion. Use singular organism names in the experiment
  sentence and plain "all offspring" observations for single-phenotype crosses.
  Added a thin gray observation-table border and genotype types alongside the
  randomized allele pairs in all three choices.
- Reworked `monohybrid_litter_inference.py` around observation, genetic setup,
  ratio interpretation, and genotype inference. A compact two-column offspring
  table now comes first, with small blue circles/brown squares, subtle row tints,
  and written counts. State the reduced phenotypic ratio explicitly; randomize
  allele letters from B, D, E, F, H, N, R, T with distinct case shapes; keep choices
  in homozygous dominant, heterozygous, homozygous recessive order, and remove the
  ambiguous-information distractor. Preserve randomized, nonrepeating scenarios
  with uniquely identifying Mendelian ratios.
- Use monospace for allele/genotype cells in the shared dihybrid and test-cross
  Punnett squares and for genotypes in the observed epistasis-cross table. Ratios,
  cross/arrows, headings, and prose retain their ordinary font.
- Simplified both directions of `epistasis_test_cross.py` to a short baseline-ratio
  introduction, two reference Punnett squares, a plain two-column observed-cross table,
  and the modified-ratio question. The table uses only F2/test-cross headers and the
  genotypes with known/unknown ratios, with horizontal scrolling on narrow screens.
  Thin gray cell borders and modest padding define the comparison without background fill.
  Separate "Standard crosses" and "Observed cross" labels, extra space before the
  observed section, and explicit observed-cross wording distinguish the reference from
  the experimental result.
  Removed repeated baseline cross/ratio labels, the genotype-class legend, and
  phenotype-grouping instructions.
- Added independent pedigree topology measurements for degree distribution, continuing branches,
  local descendant balance, and sibship variance, reusing the existing graph/count authorities.
  Two focused tests cover measurements, identity/order invariance, and shared descendants.
- Added baseline 9:3:3:1 and 1:1:1:1 Punnett squares to both directions of
  `epistasis_test_cross.py`, with shared randomized gene letters and color palettes.
  Added an uncolored observed/unknown ratio comparison without showing epistatic
  phenotype groupings, and phrased inverse questions as possible F2 outcomes.
  Retained the original "1:2:1 or 1:1:2" answers for 9:6:1 and 9:4:3 and removed
  added phenotype-ordering instructions; the baseline legend is a visual reference.

- Put the mechanism first in dihybrid gene-interaction choices, followed by plain-text
  "known as" terminology. Clarified all seven descriptions, including the 9:6:1 and
  13:3 interactions, to match the displayed phenotype groupings.
- Rotated older changelog days into `CHANGELOG-2026-09a.md` after the active log
  exceeded 800 lines, retaining the two most recent days.
- Replaced pedigree affected-sex ratio thresholds with `(M-F)^2/(M+F)`: autosomal
  scores must be below 0.25; X-linked scores must exceed 0.99 with female excess for
  dominant and male excess for recessive. Retained the two-affected minimum and all
  relationship checks. Easy matching now permits five seed offspring within its existing
  10-11-person bound; the authored XD example now has sufficient female bias. Boundary
  tests cover the new score, and the three-generation XD regression uses production policy.
- Clarified pedigree difficulty as combined size, branching, and tracing workload in module
  guidance, command help, and documentation. Existing presets already increase these controls
  together and retain their values and shared teaching checks. Removed the test requirement
  that difficulty filters must be disjoint, allowing future overlapping bands without adding
  an evidence-subtlety score.
- Require at least two affected individuals in student pedigree acceptance, rejecting 1:0
  and 0:1 counts before applying sex-balance criteria. Added boundary coverage for single
  affected individuals and the two-person minimum in X-linked and Y-linked examples.
- Moved pedigree workload tables and structural filtering into a dedicated difficulty module.
  Family connectivity now lives in the shared graph adapter and serves both layout and
  student-case selection, removing the private layout dependency and duplicate traversal code.
  Existing commands and preset values are unchanged; 21 authored/procedural case snapshots
  retained identical biological state, answers, and complete diagram geometry. Verified all
  73 focused pedigree tests and 4,633 repository tests, with two existing source-length warnings.
- Expanded the pedigree constructor with founding-couple, total-couple, and separate seed/later
  sibship bounds. Multiple founding families join through generation-two marriages into one
  connected pedigree; further unions marry in unrelated people. Construction reserves feasible
  child slots before creating people, and founder allele initialization excludes descendant-only
  joining crosses. Plain Python difficulty tables now control all constructor knobs; matching
  stays at three generations. Existing-pool filters check the same structural bounds.
  Reviewed all five inheritance modes across preset/founder-count combinations, including
  genotype transmission and HTML/SVG geometry. Verified 73 focused and 4,633 repository tests,
  reproducible runs of all three commands, desktop/phone self-tests, and a matching Blackboard
  package containing all five pedigree images.
- Promoted pedigree-to-NetworkX conversion into a shared graph adapter while keeping the
  family model authoritative. Pairwise review reuses each case's structural/visible graphs
  and neighborhood signatures within the batch, with no persistent cache or stale observation
  state. Independent graph snapshots can be edited without changing the source family.
  All 3,160 comparisons in an 80-case benchmark matched the previous results exactly;
  graph/signature construction fell from 12,640 to 160 calls. Reuse took 0.096 seconds versus
  1.18 seconds for independent comparisons locally. Verified 69 focused and 4,629 repository
  tests, including snapshot isolation and updated observations between batches.
- Added easy, medium, and rigorous pedigree workload presets shared by all three commands,
  plus a 30-40-person, five-generation bonus preset for single-pedigree identification.
  Matching remains at three generations. The same public filter selects accepted families
  from a review pool; the bands describe structural workload, not calibrated student difficulty.
  Biological and teaching acceptance stay unchanged. Larger families use feasible bounded
  sibship allocation instead of enumerating exponentially many configurations; this changes
  seeded examples while retaining reproducibility. Reviewed all five modes at every supported
  preset/format band, including valid genotype transmissions and hidden student carrier status.
  A temporary mixed pool of 5,000 accepted families took 31.27 seconds to generate, 0.25 seconds
  to filter across four bands, and 3.51 seconds to sort using the graph complexity key locally.
  Verified 68 focused and 4,628 repository tests, seeded CLI reproducibility, desktop/phone
  self-tests, and a bonus Blackboard export with its packaged diagram image.
- Added NetworkX pedigree comparison with separate topology and visible-pattern similarity,
  exact graph-isomorphism duplicate flags, and instructor-only pairwise review exports.
  Person-union graphs preserve parent/child roles and support multiple founding couples,
  disconnected components, and shared ancestry. Added complexity measures and a documented
  structural sort order without changing student question selection or inventing a cutoff.
  Verified 61 focused tests and 4,621 repository tests with two existing source-length warnings.
  A nine-example review gallery exposes separate similarity matrices and interactive complexity
  sorting; 36 pairwise comparisons took about 0.013 seconds locally. Regression fixtures cover
  joined founder families, shared ancestry, relabeling, and a neighborhood-hash collision that
  the exact isomorphism check correctly rejects.
- Increased the per-pedigree retry limit from 500 to 5,000 after three measured 500-candidate
  XD runs took 0.21-0.22 seconds each. Searches still stop at first success and fail explicitly
  on exhaustion; biological and teaching checks are unchanged.
- Investigated three-generation XD generation under the proposed squared sex-bias score.
  Raised the first-sibship limit from four to six for all three-generation modes, retaining
  random offspring sex, Mendelian transmission, and the 12-15-person matching size band.
  Raw qualifying XD candidates increased from 20/2,000 to 40/2,000; 200 seeded generation
  requests improved from six exhausted searches to zero. Production sex-balance cutoffs
  are unchanged; the investigation and regression explicitly use the proposed squared score.
  The 200 successes contained 181 distinct sex/phenotype family arrangements after ignoring
  IDs, sibling order, and reflection. Verified 54 focused tests and 4,614 repository tests
  with the two existing source-length warnings.
- Added affected-sex balance filters after the unique relationship-based teaching answer:
  autosomal absolute imbalance at most 20%, XD female excess at least 20%, and XR male
  excess above 50%, retaining the existing male-only XR teaching profile. Ratios use affected
  counts and never resolve tied teaching evidence. Instructor evidence now includes M/F counts.
  A 1,000-pedigree baseline study informed the cutoffs; another 1,000 generated under the
  filters completed without exhaustion (largest search: 63 of 500 candidates).
  Verified 53 focused pedigree tests and all 4,613 repository tests, with two existing
  source-length warnings. Temporary HTML statistics, cutoff plots, raw counts, and a filtered
  pedigree gallery document the study without adding a permanent bulk-generation test.
- Added `write_pedigree_select.py` for pattern-to-pedigree multiple choice. The choice,
  select, and match commands are thin executable orchestrators over the shared library,
  all using procedural families by default. The old match-random entry point remains compatible.
- MC diagrams now use four or five generations with 16-22 people; matching uses exactly
  three generations with 12-15 people. Construction reserves enough descendant unions
  to reach the requested depth without truncating relatives or altering Mendelian transmission.
- Verified 45 focused tests and all 4,605 repository tests (two existing source-length warnings).
  Reviewed all five inheritance modes at each supported depth, including genotype transmission
  and phenotype checks. All three browser formats work at desktop and phone widths; correct
  MC answers and 5/5 matching were verified. The new selection export packages five diagram
  images. Repaired archived changelog links to two retired pedigree tests.


### Decisions and Failures

- Followed pedigree calibration with native geometry and density probes: 8,000 accepted
  candidates, 48 rendered examples, and independent discovery/replication reviews. Width and
  parent-gap associations differed by workload; no general middle-range optimum emerged.
  Density measures duplicated width at fixed size/depth. Corrected factual review errors before
  analysis and verified SVG measurements and reflection invariance. Production ranking remains
  unintegrated; all experimental code and galleries remain in sibling `pedigree-aesthetics`.
  Verified 4,714 repository tests and two temporary geometry checks; the suite retains two
  existing source-length warnings.
- Aesthetic ranking calibration did not establish a useful simple production score. Three rounds
  of independent image reviews found redundant graph measurements and rejected two candidate
  formulas on fresh size/depth-matched examples. The latest formula won only 7 of 16 general
  validation judgments, with one tie; targeted balance comparisons alone were more favorable.
  Per the plan, production ranking and scenario conversion remain unintegrated. Experiments and
  galleries stay in sibling `pedigree-aesthetics`; its 5,000-case benchmark took 48.09 seconds to
  generate and 3.24 seconds to measure/sort. Existing inheritance and difficulty gates are unchanged.

## 2026-09-30

### Added

- Rebuilt pedigree homework around people and unions, with one Mendelian engine for simulation
  and compatibility, visible-evidence teaching profiles based on Lecture 05C, and shared layout
  for positioned HTML and editable SVG. Added editable YAML examples, cousin unions, separate
  founding families, person-bound labels, and carrier disclosure independent of simulated state.
- Migrated all three pedigree commands to one acceptance/export pipeline with explicit seeded
  verification, bounded generation failures, balanced matching sets, and instructor SVG/JSON review.
  Replaced obsolete grid codecs, duplicate validators, and old internal-API tests with focused
  biological, teaching, source, and geometry regressions. Authored `-d` now counts questions.
- Fixed hygiene discovery to skip deleted tracked files before invoking content-reading filters;
  otherwise removing the retired pedigree specification prevented full-suite collection.
- Pedigree rebuild verification: 27 focused pedigree tests plus the discovery regression passed;
  full suite passed 4,473 tests with two existing source-length warnings. Scoped pyflakes passed.
  Seeds 0-99 produced 100 visibly distinct accepted cases per mode without exhaustion (largest
  search: 18 candidates). All three commands reproduced seeded BBQ output byte-for-byte;
  self-tests accepted correct MC and 5/5 matching answers. Desktop/narrow Chromium checks confirmed
  local keyboard scrolling. Blackboard and Canvas packages each contained the expected 11 diagrams
  across three sample questions, plus a separately inspected cousin/carrier/label export.

- Added shared `--selftest` and `-O` / `--open-selftest` options using the QTI HTML
  self-test engine. Preview one random saved question in the default browser, including
  generators that call the file writer directly; BBQ and optional Blackboard ZIP remain available.

### Fixes and Maintenance

- Student pedigree commands now select one connected family per case and hide carrier status
  before evaluating the teaching answer. Removed carrier disclosure from the student legend.
  The disconnected cousin/carrier demonstration stays available in the library, while all five
  textbook patterns remain available in the student authored bank.
  Verified 32 focused tests and generated MC/self-test output without carrier markings.
  Full suite: 4,591 passed; one archived-changelog link check failed on references to
  two removed pedigree tests, unrelated to the student-output change.
- Pedigree layout now tries either side for marrying-in spouses, retaining narrower,
  collision-free maps while preserving sibling order and centered descent. Compact placement
  also penalizes stretched marriage lines. The reported four-generation family saves 29 pixels
  by moving its third-generation spouse inward; a regression protects that behavior.
  Browser comparison inspected; 31 focused tests and all 4,591 repository tests passed
  with the two existing source-length warnings.
- Replaced independent pedigree-row packing and one-way parent shifts with joint horizontal
  placement of fixed family relationships. Couples now center over their children, single-child
  descent stays vertical, and all generations participate in compact placement with label and
  symbol clearance. HTML and SVG share the corrected map. Segment construction rejects displaced
  one- or two-child groups: one child gets a straight vertical connection; two are symmetric about
  the marriage midpoint. Larger sibships allow unequal gaps around descendant branches.
  Focused regressions cover the reported alignment defects.
  Verified identical-family before/after galleries, 30 focused tests, and the full suite
  (4,590 passed; two existing source-length warnings). Matching scored 5/5 in standalone and
  local website previews at desktop and phone widths; Blackboard and Canvas packaged the
  corrected diagrams. No family relationships or inheritance rules changed.
- Varied procedural pedigree construction with one to three descendant unions across three or
  four generations, choosing feasible sibships before construction. Traits can enter through
  marrying-in founders with grandchildren. Kept genotype transmission, teaching profiles, and
  shared HTML/SVG geometry unchanged; matching now allows varied depth in both sources.
  Classed the HTML drawing table to prevent Material's automatic scrolling wrapper from
  defeating proportional sizing on narrow website previews.
- Pedigree variety verification: reviewed branching and visible inheritance clues in temporary
  galleries for all five modes and checked every displayed transmission. All 4,588 repository
  tests passed (two existing source-length warnings). All three command previews fit at
  1200, 768, and 390 pixels standalone and in local Material pages; MC and matching answers
  scored correctly. Blackboard and Canvas exports contained the expected referenced diagrams,
  and editable SVGs and packaged images were inspected. No remote publication was performed.
  All six independent audit passes completed; corrected one stale size-error message. The final
  focused suite passed 28 tests, and all three commands reproduced seeded BBQ output.
- Removed the pedigree renderer's inline scrolling wrapper and fixed minimum width after
  clarifying the no-scrollbar requirement. HTML now scales the shared geometry proportionally
  to available space, including labels and strokes; desktop and SVG geometry stay unchanged.
  The scrollbar originated in generated content, independently of website table-gutter CSS.
  Verified no diagram scrolling or cropping from 320 to 1200 pixels, including all three
  generators embedded in the locally built Material website. Full suite: 4,587 passed with
  two existing warnings; Blackboard and Canvas carrier/label images were inspected.
- Polished pedigree spacing: reduced generation spacing from 136 to 96 pixels, shortened
  child connector drops, and sized bottom padding to visible labels while retaining 32-pixel
  symbols. Shared QTI matching previews now give rich diagrams the available prompt width
  instead of the prose-width cap, so complete families are visible on desktop. Verified all
  three commands at 1200, 768, and 390 pixels, matching answers, 500 seeded cases, and
  Blackboard/Canvas images including labels and carriers. Full suite: 4,587 passed with two
  existing source-length warnings; shared QTI suite: 3,834 passed.
- Fixed Bandit B314 in the pedigree SVG regression test by using the existing lxml
  dependency with XML entity resolution and network access disabled.
- Completed six independent pedigree audit passes: Plan, Test, Style, Docs, Legacy, and
  Comment. Corrected authored-YAML and mirrored sibling-order documentation, added import
  headings, function separators, and public API docstrings, and removed brittle validation
  wording and union-index/segment-count assumptions from existing tests. Plan and Legacy
  reported no findings; no additional permanent tests were proposed. After cleanup, all
  4,473 tests passed with the two existing source-length warnings; scoped pyflakes and
  whitespace checks passed. Browser and package evidence remains from the rebuild verification.
- Isolated pedigree drawing tables from surrounding self-test and website cell
  borders and backgrounds. Fixed person-cell line height and connector sizing,
  removed the blue frame and trailing empty row, and replaced invalid paragraph
  wrappers with a scrolling container for wide pedigrees.
- Pedigree verification: 40 focused tests and scoped pyflakes passed. Chromium
  confirmed uniform 65-pixel rows under Material and competing table styles;
  desktop and narrow self-tests worked for all three generators. Blackboard
  HTML-to-image exports contained all 11 expected diagram PNGs across the three
  sample questions. Chromium required execution outside the macOS sandbox.

- Standardized allele notation in both new plant-probability generators using the
  numbered-subscript convention in *Introduction to Molecular Genetics and Genomics*,
  chapters 2 and 3. Gene letters are italic, allele numbers are subscripts, and the
  smaller number comes first in heterozygotes. The shared formatter applies this
  convention to genotype tables and cross descriptions without implying dominance.
- Standalone self-tests explicitly select the light theme so system dark mode cannot
  produce light-gray text over a white browser background.

- Declared Playwright as a direct dependency for the existing bptools image-export
  error handler and its tests. The shared export behavior is unchanged.
- Removed the stale YAML MC parser-default assertion. An omitted CLI choice count
  allows the YAML bank setting to apply before the generator falls back to five.
  Explicit CLI choice-count validation remains covered.

### Removals and Deprecations

- Removed the completed horse artwork build script, which depended on Shapely and
  a missing original chestnut SVG. Kept the editable coat-pattern SVG, finished PNG,
  and question generator that consumes the PNG.

### Developer Tests and Notes

- Allele-notation verification: all 522 plant scenarios use italic gene letters and
  numbered subscripts in the question HTML. The 35 focused plant and bptools checks,
  scoped pyflakes, desktop and 375-pixel rendering, and both CLI self-test exports passed.
  This notation update did not run the full repository suite.
- Self-test export validation: 4749 tests passed, with the two existing source-length
  advisories. Verified default-browser launch, Chromium correct-answer feedback, and
  HTML output from both shared collection and direct batch writers.

- Full `pytest tests/` run passed: 4745 tests, with the two existing source-length
  advisories for `bptools_legacy.py` and `webwork_lib.py`. No permanent tests were added.

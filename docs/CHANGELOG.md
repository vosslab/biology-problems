# Changelog

## 2026-10-01

### Changed

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

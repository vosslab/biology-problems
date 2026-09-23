# Changelog

## 2026-09-23

### Fixes and Maintenance

- Expanded MC statement YAML validation to flag malformed statement IDs and warn when a
  question form cannot supply the requested number of independent distractor groups.
- Corrected malformed statement IDs found in the Gibbs free-energy and Franklin diffraction banks.

### Behavior or Interface Changes

- Added an optional `num_choices` YAML setting for per-bank defaults; `-c` overrides it, and the
  generator still defaults to five choices when the setting is absent.
- Set four-choice defaults for the enzyme-inhibitor, G-U wobble, mRNA-processing, and
  nucleotide-components banks, which have three usable distractor groups per item.

- Labeled horse genotypes by coat pattern and made the illustration and offspring table render
  cleanly in ordinary HTML layouts.
- Added a short hint that directs students to use lethal-white and fewspot counts in sequence.

## 2026-09-22

### Additions and New Features

- Added a randomized horse coat-pattern genotype-inference question with six curated crosses,
  offspring counts, and an editable three-coat SVG with a Blackboard-compatible PNG rendering.
- Renamed the horse question generator to `horse_coat_pattern_inference.py`; kept `horses.py` as a
  compatibility launcher.
- Added `-c` / `--num-choices` to the multiple-choice statements BBQ generator for an explicit
  total answer count, including the correct choice.
- Added the shared five-choice default and `-c` / `--num-choices` handling to the complementary
  sequences multiple-choice generator.
- Connected `chargaff_dna_percent.py` to its existing `--num-choices` option, supporting two to six
  answer choices including the correct answer.
- Rendered restriction-enzyme overhang sequence choices in a monospace font.

### Behavior or Interface Changes

- Explicit choice counts require enough distinct distractor groups; questions without enough groups
  are skipped. The default is five total choices, including the correct choice.

### Developer Tests and Notes

- Added focused checks for requested choice counts, unavailable distractors, and CLI validation.
- Added coverage for complementary-sequence MC choice counts in both direction modes.
- Added coverage for the Chargaff generator's requested and default choice counts.

## 2026-09-20

### Additions and New Features

- Added shared `-I` / `--html-to-image` for opt-in `-B` Blackboard exports, converting supported
  HTML drawings into packaged PNGs while retaining normal BBQ output and export-failure safeguards.
- Added `circular_digest.py`, a randomized circular-DNA restriction digest generator with an
  orange rounded-rectangle plasmid map, a 0 kb origin occupied by the non-selected enzyme, and
  colored enzyme labels inside the DNA path for image-exported Blackboard pools.
- Added `digest_lib.py` for common restriction-digest argument parsing and distinct enzyme-label
  selection, plus `dna_render_lib.py` for shared inline-CSS DNA-map primitives.

### Behavior or Interface Changes

- Made `-I` reject use without `-B` / `--bbexport`, and routed every legacy direct writer and
  YAML-to-BBQ converter through the shared image-export option.
- Made `-d` request accepted questions from single-question generators, with bounded redraws for
  rejected or duplicate attempts; batch generators retain their existing attempt-based behavior.
- Made every linear-digest difficulty default valid for either the finite-fragment or longer-strand
  presentation, preserving the minimum two selectable gel-band lengths.
- Shortened the generated linear-digest filename component from `length_` to `len_`.
- Made randomized 16 kb rigorous linear-digest maps deliberately produce co-migrating equal-length
  fragments, while retaining the single-enzyme, two-enzyme-label MA band-length model.
- Added `-E`, `-M`, and `-R` aliases for the standard easy, medium, and rigorous difficulty flags.
- Moved the restriction-enzyme source paragraph to the opening of linear and circular
  digest questions.
- Spread restriction-enzyme map colors to navy `#0067cc` and teal `#00775f`.
- Restored a dashed orange DNA continuation past both ends of linear strand maps,
  and counted strand outside pieces only for the selected enzyme.

### Fixes and Maintenance

- Rebuilt both restriction maps around the shared rendering primitives: linear maps now align
  colored labels and 3 px by 16 px ticks to black coordinates, while circular maps use a thick
  rounded rectangle with outside coordinates and inside enzyme labels.
- Lengthened restriction-map ticks from 8 px to 16 px so they extend past the DNA stroke;
  thickness stays 3 px.
- Gave enzyme-labeled ticks 4 extra pixels toward the label, leaving unlabeled coordinate
  ticks at the shared 16 px length.
- Mapped circular-digest coordinates onto the complete rounded-rectangle centerline, with a
  tick and outside kb label at every integer, continuous corner normals, and enzyme names
  only at restriction sites whose true coordinates fall on straight edges.
- Tightened top and bottom circular-map labels toward their ticks by offsetting along the
  local normal by tick length plus the label's half-size, instead of one gap for every side.
- Kept corner integer-kb marks as ordinary black coordinate ticks, and required enzyme sites
  to sit on straight edges with label clearance from the rounded corners.
- Restored the non-selected enzyme site at 0 kb so the origin is a real restriction mark
  for the distractor enzyme, not a cut for the enzyme in the question.
- Lowered the circular-digest medium and rigorous presets to 2 sites per enzyme so labeled
  coordinate ticks still outnumber restriction annotations.
- Sampled circular restriction sites like the linear digest, keeping corners enzyme-free and
  0 kb as a distractor site, preferring spread maps whose two enzymes yield different bands.
- Tightened the circular and linear map canvases around the labeled diagram so less empty
  space sits between the figure and the following question text.
- Colored restriction-enzyme names in the question stem with the same map colors used on
  the DNA diagrams.
- Added a short source paragraph for the two restriction enzymes on linear and circular
  digest questions, matching the overhang-question context style.
- Added [CUT_PLACEMENT.md](../problems/molecular_biology-problems/restriction_enzymes/CUT_PLACEMENT.md)
  as the teaching contract for restriction-digest maps: place, evaluate, then
  search, with easy, medium, and rigorous band-set targets for linear and
  circular questions.
- Made linear medium default to 3 selected sites on a 12 kb fragment, circular
  medium and rigorous default to 3 selected sites with 2 distractor sites, and
  required `shared_correct_fraction <= 0.5` plus selected-enzyme co-migration
  only at rigorous.
- Gave graphical DNA strokes and ticks non-empty `&nbsp;` content and a relative inner canvas
  div so Blackboard HTML-to-image export does not serialize empty spans as self-closing XML
  that Chromium then drops.
- Recorded Blackboard HTML simplicity guidance in [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md).
- Added a separate restriction-enzyme idea note for future diagnostic-digest, inference, RFLP,
  co-migration, and map-validation question families without changing the linear MA generator.
- Synchronized shared style guides, tests, and repository support files from the starter template.

### Developer Tests and Notes

- Added focused coverage for parsing, invalid export combinations, and the qti-package-maker
  `html_to_image` option handoff.
- Added parser coverage for the `-E`, `-M`, and `-R` difficulty aliases, and dropped the linear
  table-cell-count test after that grid renderer was replaced.
- Added circular-map checks that 0 kb is top-center, integer kb use the full centerline
  perimeter, and enzyme-eligible coordinates are straight-edge integers.

## 2026-09-17

### Fixes and Maintenance

- Preserved whitespace immediately before removed outer `</strong>` wrappers around strict color
  spans so PGML replacement output does not join adjacent words.

## 2026-09-09

### Additions and New Features

- Added shared `-B` / `--bbexport` generation of validated Blackboard pool ZIPs through the
  `qti_package_maker` library while retaining the source BBQ text, with explicit rejection of item
  types the export engine cannot write.

### Behavior or Interface Changes

- Made hidden decoy terms and the no-click wrapper opt-in for Blackboard Learn Original so normal
  generator output avoids those two Ultra-incompatible anti-cheat transformations by default.
- Kept only the positive `--hidden-terms`, `--noclick-div`, and `--bbexport` opt-ins; their former
  negative flags only restated the new defaults.
- Routed seven batch generators, three YAML-to-BBQ converters, and the older four-point gene-map
  generator through the shared export-aware writer.

### Fixes and Maintenance

- Synchronized shared style guides, tests, and repository support files from the starter template.
- Ignored generated `blackboard_export_zip-*.zip` artifacts alongside existing BBQ and QTI output.
- Updated the README, architecture, and file-structure descriptions for Blackboard pool ZIP output,
  and gave the known-incomplete four-point generator a typed `main()` entrypoint without changing
  its question algorithm.

### Developer Tests and Notes

- Added behavioral coverage for shared parser opt-ins, generator-level anti-cheat locks,
  Ultra-compatible default markup, the export handoff, and failure preservation for unsupported
  ORDER questions; package-structure validation remains owned by `qti-package-maker`.
- Verified standard single-question, batch, and YAML generators produce retained BBQ text plus
  readable Blackboard exports containing their expected pool data; the full suite passes 4,526
  tests under Python 3.12.

## 2026-08-27

### Fixes and Maintenance

- Synchronized shared style guides, tests, and repository support files from the starter template.

## 2026-08-25

### Fixes and Maintenance

- Removed named Arial font overrides from generated questions, review pages, debug pages, and
  canvas labels so normal text inherits the host site's typography; replaced the DNA gel image's
  Arial Narrow candidate with the existing PT Sans fallback, removed generic sans-serif overrides
  from ordinary HTML and inline SVG labels, and normalized intentional fixed-width content from
  Courier-first stacks to generic monospace.
- Removed clock-dependent, inventory, prompt-copy, and HTML-fragment smoke tests that did not meet
  the permanent pytest checklist; moved the repo-wide Bandit scan to a direct maintainer script so
  the fast pytest lane no longer launches an external security subprocess.

## 2026-08-19

### Fixes and Maintenance

- Replaced removed `numpy.chararray` uses in the shared phylogenetic-tree renderer with modern
  NumPy arrays, restoring gene-tree question generation under NumPy 2.5.
- Added required `topic` metadata to five multiple-choice statement banks, restoring their PGML
  conversions.

## 2026-07-15

### Additions and New Features

- Added a minimal WeBWorK multiple-choice example asking for a favorite color.

## 2026-07-14

### Behavior or Interface Changes

- Rebuilt `README.md` as a newcomer-focused landing page with a representative generated question,
  outcome-oriented capabilities, a complete first-run path, curated documentation routes, setup
  limitations, current catalog status, and the repository's code and educational-content licenses.
- Linked the public Biology Problems OER collection, the published `qti-package-maker` package, and
  its development repository from the landing page, and added a repository clone command to Quick
  start.
- Made the published `qti-package-maker` distribution the primary install path, removed its import
  name from `pip_requirements.txt` so it can be released independently, retained sibling checkout
  guidance for joint development, and kept the personal environment helper unchanged.
- Clarified that `biology-problems` runs directly from a source checkout rather than as an installed
  Python package, and removed stale `pyproject.toml` and PyPI-packaging references from the active
  architecture and file-structure documentation.

## 2026-07-12

### Behavior or Interface Changes

- Re-audited the full 178-generator and 98-YAML topic-classification inventory
  under a broad multi-subject policy. Each concrete task variant may appear in
  every applicable subject but is limited to one chapter per subject.
- Added validation that preserves multi-subject assignment rows, verifies all
  subject/chapter routes, rejects same-subject chapter duplication, detects
  exact duplicate rows, and requires complete frozen-inventory coverage.

### Fixes and Maintenance

- Prevented the lipid chemical-formula generator from emitting duplicate rendered
  answer choices when distinct molecule names share a formula, and repaired an
  unclosed list item in the pentapeptide Wordle question HTML.
- Removed a duplicated ANOVA hypothesis-pair distractor and added rendered-choice
  uniqueness checks across all hypothesis statement question variants.
- Added non-empty topics to the potential-versus-kinetic-energy and membrane
  diffusion statement banks so their PGML generators pass metadata validation.
- Reworded lethal-allele ratio choices to avoid downstream colon-delimiter
  collisions, and replaced the gene-therapy matching bank's malformed named
  colors with quoted XML-safe colors from the WCAG-audited repository palette;
  removed broad replacements that split `genetic` and `adenovirus`.
- Expanded lethal-allele questions with heterozygote-by-normal crosses so
  lethal fractions, survival fractions, counts, and living phenotype ratios
  vary across genetically valid scenarios.
- Reworked lethal-allele variation around explicit Punnett probabilities,
  deriving twelve question forms for conception outcomes, conditional survivor
  fractions, counts, and both phenotype-ratio directions.
- Replaced malformed named colors in the population-genetics matching bank
  with quoted XML-safe colors from the WCAG-audited repository palette, and
  replaced an unrelated Theranos description with valid random-mating definitions.
- Audited all matching-set YAML colors against white at WCAG AA, darkened 23
  failing hex occurrences across seven banks, and replaced remaining named CSS
  colors in six banks with documented values from the audited palette.
- Stopped the DNA profiling father and killer generators from writing unused
  per-question diagnostic PNG files into the current working directory.
- Added explicit uppercase color-name comments to all 486 previously
  uncommented color replacement rules across 39 matching-set YAML banks.
- Prevented rare chi-square division-by-zero scenarios by redrawing zero-count
  observed classes, and constrained DNA gel calibration curves so every marker
  in the declared range has a positive migration distance; each gel question
  now receives its own calibration curve so high-volume runs meet their target.
- Bounded chi-square observed-count redraws at 1,000 attempts with an explicit
  failure instead of relying on an unbounded retry loop.
- Curated 432 final task assignments, filled all 49 previously unassigned
  sources, corrected several existing chapter placements, and documented 189
  changes plus all resolved chapter ambiguities without running a new automated
  classifier.
- Rotated older changelog day blocks into `docs/CHANGELOG-2026-06a.md`, keeping
  the two newest dated blocks active under the repository rotation policy.

### Developer Tests and Notes

- Added focused assignment-loader and task-validation tests and recorded the
  frozen inventory, chapter routing, curation changes, ambiguity decisions, and
  final coverage report under `topic_classifier/`.
- Added `docs/GENERATOR_SCENARIO_LIMITS.md` to distinguish intentional finite
  question banks from duplicate-attempt shortfalls and stale generated output.
- Enumerated and shuffled hypothesis scenario, tail, and answer-order combinations
  before generation, and expanded Kaleidoscope mapping into six shuffled four- and
  five-band scenarios while allowing mixed-mode retries to advance past duplicates.
- Added a shipped restriction-enzyme web-data cache with full labeled REBASE fields
  and automatic per-enzyme six-month refreshes so overhang generators avoid hundreds
  of repeated HTTP requests during normal generation.
- Populated the cache with all 280 eligible enzymes, resolved it through
  `bptools.get_repo_data_path()`, and measured warm-cache generation at about
  2.7 seconds for 191 overhang-sequence or 280 overhang-type questions.
- Made the unordered two-gene tetrad distance validations use identical arithmetic
  ordering, preventing valid boundary cases from failing because of floating-point
  representation differences around the existing 0.04 tolerance.
- Replaced rigorous gene-tree matching's repeated ranking of roughly 1.3 million
  trees with bounded random samples of 1,024 unique labeled trees, and selected
  random taxa orders directly instead of enumerating all 40,320 permutations.
  This preserves the full topology and label space while removing the main
  per-question performance bottlenecks.
- Removed the artificial two-question cap from the DNA melting-temperature
  generator. Each question now randomly selects the highest- or lowest-melting
  concept and generates fresh fixed-length sequences with clearly separated GC
  contents.
- Grouped the overhang generators and restriction-enzyme library under
  `problems/molecular_biology-problems/restriction_enzymes/`.

## 2026-07-03

### Additions and New Features

- Added `docs/COLOR_CONTRAST_ACCESSIBILITY.md` (generic WCAG contrast method) and
  `docs/PALETTE_CONTRAST_AUDIT.md` (14-color rainbow palette, other problem colors, non-palette
  replacements, and a YAML custom-color note), with ratios measured via
  `tools/contrast_calculator.py`.

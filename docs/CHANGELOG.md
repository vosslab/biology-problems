# Changelog

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

## 2026-07-03

### Additions and New Features

- Added `docs/COLOR_CONTRAST_ACCESSIBILITY.md` (generic WCAG contrast method) and
  `docs/PALETTE_CONTRAST_AUDIT.md` (14-color rainbow palette, other problem colors, non-palette
  replacements, and a YAML custom-color note), with ratios measured via
  `tools/contrast_calculator.py`.

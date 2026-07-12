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

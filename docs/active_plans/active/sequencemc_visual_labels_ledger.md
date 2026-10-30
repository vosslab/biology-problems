# SEQUENCEMC visual labels ledger

## Approved scope

Add `-l/--label-style` to YAML SEQUENCEMC with bracketed (default), numbers, roman,
roman-lower, circled (up to 20), dice (up to 6), lowercase Greek (up to 24), and words. Add
`-C/--color-mode` with full (default), labels, and none. Use the documented fixed palette,
with the prescribed four- and six-step subsets, evenly spaced entries for other lengths through
14, and cycling for longer sequences. Assign colors after display shuffling. Keep all four
choices complete, preserve replacement behavior and explicit authored colors, leave molecular
structures and ordered molecule-name clues unchanged, and keep native ORDER schemas and filenames.

## Ownership and status

- Owner: implementation agent, all code, tests, docs, and this ledger.
- Status: complete; specification, quality, and integration reviews accepted.
- Files: `problems/ordering/orderinglib.py`,
  `tests/yaml/test_ordering_yaml_generators.py`,
  `problems/ordering/ORDERING_AUTHORING_GUIDE.md`, `docs/COLOR_PALETTE.md`,
  `docs/CHANGELOG.md`.
- No commits. Preserve any concurrent edits; initial working tree was clean.

## Decisions

- Use the live `string_functions.number_to_roman` and `bptools.number_to_cardinal` helpers.
- Render HTML entity tokens for circled numbers, dice, and Greek letters to retain ASCII source.
- Suppress browser ordered-list markers and render explicit labels so every choice uses the same
  visible token. Render arrows without color.
- Keep colors tied to shuffled positions, never to the answer's biological or procedural order.

## Verification

- Permanent-test review: keep the numeric-step/replacement behavior, MC answer reconstruction
  and native ORDER behavior, choice-to-prompt color consistency, and full/labels/none color-mode
  behavior. Remove exact label-token and palette inventories, all-style exhaustive rendering,
  and capacity/error-wording checks: these pin implementation details or completed feature proof
  without distinct durable protection. The color-consistency assertion now uses a matching regex
  and compares the complete mapping, so it cannot pass vacuously.
- Integration review: found and fixed a gap in the full-mode assertion. It now strips only the
  label span and confirms that prompt prose remains colored, reciprocating the labels-mode check
  that confirms prompt prose is uncolored. The four retained tests remain behavior-focused rather
  than pinning label or palette inventories.
- Pass after pruning: `source source_me.sh && python3 -m pytest tests/yaml/test_ordering_yaml_generators.py` (4 tests).
- Full suite: `source source_me.sh && pytest tests/` (5,775 passed; three unrelated failures
  from missing `LICENSE.CC-BY-SA-4.0` targets in three existing README files). The target is
  absent at HEAD (`git show HEAD:LICENSE.CC-BY-SA-4.0` exits 128).
- Pass: generated prose and glycolysis SEQUENCEMC self-test HTML plus Blackboard pool ZIPs in
  `/private/tmp`; ZIP inventories are readable. The HTML preserves the molecule-name clue and
  structure script, and the prose preview shows hidden list markers plus position-consistent
  label colors. Glycolysis self-test reports that `format_html_lxml()` skips JS syntax checks;
  direct browser rendering was not performed.
- Pass: verified native ORDER help does not expose MC-only label/color flags.
- Pass: rotated changelog with `devel/rotate_changelog.py`; active file now contains two newest
  day blocks, with history preserved in `CHANGELOG-2026-10b.md` and `CHANGELOG-2026-10c.md`.
- Specification review: accepted with no blockers.
- Quality review: accepted with no blockers. Reviewed presentation
  validation, label generation and capacities, palette selection, shuffled-position
  assignment, complete choice rendering, color modes, native ORDER isolation, tests,
  authoring guidance, palette documentation, and changelog rotation. Confirmed the
  only `parse_arguments()` caller passes the MC/native mode, so native help remains
  free of the MC-only options. `git diff --check` passes.
- Integration review: accepted after the full-mode prose-color assertion was added.
  This task reran the focused YAML ordering test and `git diff --check`; the full suite was
  not rerun. The earlier full-suite result and integration limits above remain the recorded
  evidence.
- Integration limitation: generated glycolysis output passed its self-test and package
  inventory checks, but direct browser rendering and LMS import were not verified.

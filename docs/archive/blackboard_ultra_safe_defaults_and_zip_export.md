# Blackboard Ultra-safe defaults and ZIP export

## Summary

This is a modest change: one central implementation in `bptools.py`, plus migration of 11 legacy
output paths. All Blackboard-question generators default to Ultra-compatible anti-cheat markup and
accept `-B` / `--bbexport`.

No `pyproject.toml` will be created or changed.

## Interface and behavior

- Default hidden terms and the no-click wrapper to off. Retain `--hidden-terms` and
  `--noclick-div` as explicit opt-ins for retired Blackboard Learn Original; these compatibility
  flags may be deprecated if that path is retired.
- Preserve per-generator `allow_insert_hidden_terms = False` and `allow_no_click_div = False` locks
  so incompatible generators still cannot enable those features.
- Add shared `-B` / `--bbexport`, defaulting to no export.
- When enabled, write `bbq-<name>-questions.txt`, then use the `qti_package_maker` library API to
  read that file and create `blackboard_export_zip-<name>.zip` beside it.
- Keep both files. Propagate conversion errors, retain the BBQ text for diagnosis, and report
  success after validating the ZIP.
- Derive supported question types from the Blackboard export engine. Its current writers support
  `MC`, `MA`, `MATCH`, `FIB`, `MULTI_FIB`, and `NUM`; reject other types such as `ORDER` with a clear
  error instead of silently producing an incomplete package.
- Validate that the generated filename follows the existing `bbq-<name>-questions.txt` contract
  before deriving the adjacent ZIP name. This is a naming-contract boundary, not a shell-injection
  defense; conversion uses boolean `argparse` choices and direct library calls. These rules document
  and validate expected input structure under ASVS 2.1.1 and 2.2.1.
- Build the ZIP at a temporary adjacent path, validate its structure, and atomically replace the
  destination. Failed conversion removes the temporary ZIP, preserves the BBQ file, and leaves no
  newly created partial destination ZIP.

## Implementation changes

- Add an export-argument helper and Blackboard-export helper to `bptools.py`; have
  `make_arg_parser()` and `collect_and_write_questions()` use them automatically.
- Extend `write_questions_to_file()` with an optional `bbexport=False` parameter for batch and
  custom generators.
- Route the seven batch generators, three custom YAML-to-BBQ converters, and the older four-point
  gene-mapping generator through the shared export-aware writer.
- Leave the unused `bptools_legacy.py` archive unchanged; it has no live callers.
- Update `docs/USAGE.md` with the Ultra-safe defaults, legacy opt-ins, `--bbexport` example, output
  names, and supported-type limitation. Record the change under 2026-09-09 in
  `docs/CHANGELOG.md`.

## Test plan

- Keep permanent behavior tests for explicit legacy opt-ins, generator-level locks,
  default emitted markup, the bptools export handoff, and rejection/preservation for unsupported
  question types. Leave Blackboard package-format coverage to `qti-package-maker`.
- As one-time rebuild evidence, inspect parser defaults; convert a minimal BBQ file and verify both
  outputs, ZIP readability, `imsmanifest.xml`, and Blackboard pool data; run representative
  single-question, batch, and YAML generators with `--help` and `--bbexport`; verify the incomplete
  four-point generator's new options with `--help`; and confirm generated artifacts remain ignored
  and untracked.
- Run the permanent suite with
  `source source_me.sh && /opt/homebrew/opt/python@3.12/bin/python3.12 -m pytest tests/`.

## Resolved review questions

- The 11 legacy paths are the seven callers of `collect_question_batches()` followed by
  `write_questions_to_file()`, the three `yaml_*_to_bbq.py` converters that write files directly,
  and `four_point_test-cross_gene_map-distances_plus.py`. The four-point generator is a known
  incomplete four-gene version, so this change adds its CLI and shared-writer plumbing without
  treating successful question generation as an acceptance gate.
- "Ultra-compatible anti-cheat markup" has a narrow meaning. The hidden-term feature injects
  visually hidden spans whose text becomes visible when Ultra strips their CSS, and the no-click
  wrapper injects event-handler attributes that Ultra strips. Disabling both prevents those two
  known corruptions. It does not claim that each generator's authored color, script, or table layout
  survives Ultra; [the showcase catalog](../active_plans/reports/ultra_classic_showcase_question_catalog.md)
  documents those separate limitations.
- The `qti_package_maker` public interface reads BBQ into an item bank and saves through the
  `blackboard_export_zip` engine. The writer module itself is the authority for supported types.
- `write_questions_to_file()` is the narrow shared boundary: the standard single-question path
  already converges there internally, while the 11 paths above can call its public wrapper without
  changing their question-generation logic.
- Parser/helper tests cover durable behavior. Representative `--help`, ignore-state, and generator
  runs remain one-time implementation evidence, with one real generator export as the primary
  end-to-end proof.

## Assumptions

- "Universal" means every current generator that produces BBQ question text; PG/PGML-only
  utilities do not perform Blackboard export.
- `qti_package_maker` remains an external installed dependency or sibling checkout loaded by
  `source_me.sh`.
- The library API is authoritative and replaces invoking a hard-coded
  `~/nsh/.../bbq_converter.py` subprocess.

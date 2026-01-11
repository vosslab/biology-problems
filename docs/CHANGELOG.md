# Changelog

## 2026-01-11
- Expanded [problems/biochemistry-problems/Henderson-Hasselbalch.py](problems/biochemistry-problems/Henderson-Hasselbalch.py) to support `-t` question types `pH`, `pKa`, and `ratio` (numeric or MC formats) in addition to `equation`, using the shared biochemistry buffers library for acid/base scenarios.
- Updated Henderson-Hasselbalch concentration units to M/mM/&mu;M for intro-biochemistry readability and aligned repo-root resolution with the shared bptools git-root helper.
- Removed the optional `bptools` import fallback in [problems/biochemistry-problems/Henderson-Hasselbalch.py](problems/biochemistry-problems/Henderson-Hasselbalch.py); `bptools` is now required at import time.
- Added pytest coverage for Henderson-Hasselbalch calculation helpers in [tests/libs/test_henderson_hasselbalch.py](tests/libs/test_henderson_hasselbalch.py).
- Fixed PubChem SMILES fetching to handle current PubChem REST responses that provide `SMILES` instead of `IsomericSMILES` in [problems/biochemistry-problems/PUBCHEM/pubchemlib.py](problems/biochemistry-problems/PUBCHEM/pubchemlib.py).
- Moved PubChem molecule persistence from a local cache file to [data/pubchem_molecules_data.yml](data/pubchem_molecules_data.yml) (with automatic migration from the legacy `cache_pubchem_molecules.yml`).
- Expanded [problems/biochemistry-problems/PUBCHEM/which_amino_acid_mc.py](problems/biochemistry-problems/PUBCHEM/which_amino_acid_mc.py) to support a FIB mode (`--fib`) in addition to MC.
- Added a small pytest for PubChem SMILES extraction in [tests/libs/pubchem/test_pubchem_smiles_extraction.py](tests/libs/pubchem/test_pubchem_smiles_extraction.py).
- Fixed `--ma` default choice handling in [problems/biochemistry-problems/alpha_helix_h-bonds.py](problems/biochemistry-problems/alpha_helix_h-bonds.py) so MA no longer errors unless the user explicitly sets `-c/--num-choices` below the minimum.
- Simplified the metabolic pathway HTML table layout in [problems/biochemistry-problems/metaboliclib.py](problems/biochemistry-problems/metaboliclib.py) to avoid extra empty columns in text previews.
- Expanded the example pools for hydrophobic/hydrophilic compounds in [problems/biochemistry-problems/which_hydrophobic-simple.py](problems/biochemistry-problems/which_hydrophobic-simple.py) to be more obvious for intro students.
- Refactored `bptools.make_outfile(...)` so the base filename always comes from `sys.argv[0]` and positional args are suffix parts (legacy leading `None`/`__file__` arguments are ignored), preventing cross-script output filename collisions like `bbq-MC-questions.txt`.

## 2026-01-09
- Updated [docs/CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) with expanded component descriptions, clearer data flow, testing details, and known gaps.
- Updated [docs/FILE_STRUCTURE.md](FILE_STRUCTURE.md) with current top-level layout, comprehensive library module listings, tools/tests directory details, and practical guidance for adding new work.

## 2026-01-06
- Updated the phylogenetic tree gene tree choice/match generators to use the shared
  bptools question framework with standard args, hint handling, and outfile helpers:
  [problems/inheritance-problems/phylogenetic_trees/gene_tree_choice_plus.py](problems/inheritance-problems/phylogenetic_trees/gene_tree_choice_plus.py),
  [problems/inheritance-problems/phylogenetic_trees/gene_tree_matches_plus.py](problems/inheritance-problems/phylogenetic_trees/gene_tree_matches_plus.py).
- Refactored PubChem biochemistry generators to use the shared bptools question framework
  (standard args, outfile helpers, and shared collection utilities):
  [problems/biochemistry-problems/PUBCHEM/match_amino_acid_structures.py](problems/biochemistry-problems/PUBCHEM/match_amino_acid_structures.py),
  [problems/biochemistry-problems/PUBCHEM/order_glycolysis_molecules.py](problems/biochemistry-problems/PUBCHEM/order_glycolysis_molecules.py),
  [problems/biochemistry-problems/PUBCHEM/polypeptide_fib_sequence.py](problems/biochemistry-problems/PUBCHEM/polypeptide_fib_sequence.py),
  [problems/biochemistry-problems/PUBCHEM/which_amino_acid_mc.py](problems/biochemistry-problems/PUBCHEM/which_amino_acid_mc.py),
  [problems/biochemistry-problems/PUBCHEM/which_macromolecule.py](problems/biochemistry-problems/PUBCHEM/which_macromolecule.py),
  [problems/biochemistry-problems/PUBCHEM/wordle_peptides.py](problems/biochemistry-problems/PUBCHEM/wordle_peptides.py).
- Added lightweight pytest coverage for PubChem generator text builders and local data loaders in
  [tests/libs/pubchem/test_pubchem_generators.py](tests/libs/pubchem/test_pubchem_generators.py).
- Added lightweight pytest coverage for biostatistics box plot generators in
  [tests/libs/biostatistics/test_biostatistics_boxplots.py](tests/libs/biostatistics/test_biostatistics_boxplots.py).

## 2026-01-05
- Fixed pyflakes issues across multiple generators (unused imports/variables, missing helper functions, and indentation errors).
- Converted a number of `.format(...)` string constructions to f-strings in the touched files.
- Updated gene mapping scripts to import `gene_map_class_lib` after the genemap class library rename.
- Added a solver library for unordered tetrad three-gene problems and wired it into the generator for answer verification.
- Updated the bptools audit to treat python files under *lib/ directories as libraries.
- Moved the pedigree layout smoke test into `tests/` and converted it to a pytest.
- Reorganized pedigree helpers under `problems/inheritance-problems/pedigrees/pedigree_lib/` and updated imports, tests, and docs (including a `code_definitions.py` rename to avoid stdlib `code` conflicts).
- Added a pedigree genetic validation module for autosomal dominant/recessive key-evidence checks (affected-parent/unaffected-child and unaffected-parent/affected-child patterns).
- Added `genetic_assignment.py` to evaluate which inheritance modes (AD/AR/XLD/XLR/YL) are consistent with a pedigree graph spec.
- In genetic assignment, explicit carrier statuses now constrain possible modes to recessive inheritance (AR/XLR).
- Updated `cat_pedigree_lib.py` to import pedigree helpers from `pedigree_lib/` after the reorg.
- Clarified in `PEDIGREE_SPEC_v1.md` that union partner tokens are bare IDs only (no sex/status tokens).
- Clarified in `PEDIGREE_SPEC_v1.md` that each union must include a previously defined partner and that marry-ins are assumed unaffected with sex inferred.
- Clarified in `PEDIGREE_SPEC_v1.md` that founder-descendant unions are allowed, founder-undefined unions are invalid, and unions may not introduce two undefined partners.
- Removed de novo language from pedigree validation docs and APIs (AD now always requires an affected parent).
- Tightened autosomal constraint propagation in `genetic_assignment.py` by pruning parents after updated child domains.
- Reworked `genetic_assignment.py` to use tuple-based allele representations for autosomal and X-linked modes.
- Added XLD/XLR/YL genetic constraint validators in `genetic_validation.py`.
- Strengthened XLR/XLD constraint checks in `genetic_validation.py` when carriers are visible.
- Added pytest coverage for `genetic_assignment.py` and `genetic_validation.py`.
- Expanded `genetic_assignment.py` pytest coverage for carrier-visible, XLR, and Y-linked edge cases.
- Added pytest coverage for additional X-linked and autosomal recessive edge cases in pedigree genetics validation.
- Updated docs, tests, and index-builder tools after moving generators under `problems/` (including relocating `problems/multiple_choice_statements/`).
- Added pytest coverage for `bptools.py` helpers and test harness setup (`tests/test_bptools.py`, `tests/conftest.py`).
- Added focused pytest coverage for `bptools.applyReplacementRulesToText` / `bptools.applyReplacementRulesToList` and key helpers in `problems/multiple_choice_statements/yaml_to_pg.py`.
- Added pytest coverage for YAML-driven content builders in `matching_sets/` and `problems/multiple_choice_statements/` (including `yaml_multiple_choice_statements.py` and `yml_to_pgml.py`).
- Added `docs/QUESTION_FUNCTION_INDEX.md` and `tools/build_question_function_index.py` to track question-creator functions and their Git creation dates.
- Improved `tools/build_question_function_index.py` to better trace function origins across renames/moves and to show daily headings (YYYY-MM-DD), skipping symlink shims and using file “first seen” fallback dates when true file-add commits aren’t available.
- Renamed the Kaleidoscope ladder helper module to
  [problems/biochemistry-problems/kaleidoscope_ladder/protein_ladder_lib.py](problems/biochemistry-problems/kaleidoscope_ladder/protein_ladder_lib.py) and added a compatibility shim
  [problems/biochemistry-problems/kaleidoscope_ladder/ladder.py](problems/biochemistry-problems/kaleidoscope_ladder/ladder.py).
- Added a preliminary Kaleidoscope ladder mapping generator in
  [problems/biochemistry-problems/kaleidoscope_ladder/kaleidoscope_ladder_mapping.py](problems/biochemistry-problems/kaleidoscope_ladder/kaleidoscope_ladder_mapping.py) with mapping + unknown-size estimate questions and pytest coverage.
- Added a lane-based Kaleidoscope gel question generator in
  [problems/biochemistry-problems/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band_mw.py](problems/biochemistry-problems/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band_mw.py) (Lane 1 ladder, Lane 2 unknown band), including too-short/too-long run scenarios.
- Added an MC-only Kaleidoscope gel question generator that uses real protein MWs but anonymous lane labeling in the prompt:
  [problems/biochemistry-problems/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band_protein_mc.py](problems/biochemistry-problems/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band_protein_mc.py).
- Updated the Kaleidoscope ladder scripts to use the standard `bptools.make_arg_parser` / `bptools.collect_and_write_questions` CLI framework (default `-d 2` questions).
- Removed custom `-o/--outfile` CLI overrides so Kaleidoscope ladder scripts use the standard `bptools.make_outfile(None)` naming.
- Refactored additional legacy generators to the standard `bptools.make_arg_parser` / `bptools.collect_and_write_questions` single-question framework:
  [problems/biochemistry-problems/buffers/pKa_buffer_state.py](problems/biochemistry-problems/buffers/pKa_buffer_state.py),
  [problems/biochemistry-problems/fret_permute_colors.py](problems/biochemistry-problems/fret_permute_colors.py),
  [problems/biochemistry-problems/macromolecules_categorize_by_name.py](problems/biochemistry-problems/macromolecules_categorize_by_name.py),
  [problems/biochemistry-problems/photosynthetic_light_pigments.py](problems/biochemistry-problems/photosynthetic_light_pigments.py),
  [problems/biochemistry-problems/quick_fatty_acid_colon_system.py](problems/biochemistry-problems/quick_fatty_acid_colon_system.py),
  [problems/biostatistics-problems/busse_woods_anova.py](problems/biostatistics-problems/busse_woods_anova.py),
  [problems/biostatistics-problems/busse_woods_two_sample_f_test.py](problems/biostatistics-problems/busse_woods_two_sample_f_test.py),
  [problems/inheritance-problems/blood_type_mother.py](problems/inheritance-problems/blood_type_mother.py),
  [problems/inheritance-problems/blood_type_offspring.py](problems/inheritance-problems/blood_type_offspring.py),
  [problems/inheritance-problems/polyploid/polyploid-gametes.py](problems/inheritance-problems/polyploid/polyploid-gametes.py),
  [problems/inheritance-problems/punnett_choice.py](problems/inheritance-problems/punnett_choice.py),
  [problems/inheritance-problems/translocation/robertsonian.py](problems/inheritance-problems/translocation/robertsonian.py).
- Added `tools/audit_problem_scripts_bptools_framework.sh` to bin `problems/` scripts into bptools-framework vs non-framework lists.
- Extended the audit output to also list script-like files missing a python shebang and/or an `if __name__ == "__main__":` guard.
- Extended the audit output to also list python-shebang files under `problems/` that are not marked executable (+x).
- Added `tools/audit_problem_scripts_bptools_framework.py` and made the `.sh` a thin wrapper so the audit runs consistently on macOS (and now also separates batch-style vs single-question scripts).
- Updated the audit to ignore python files under `.venv/` directories.
- Updated the audit to skip writing empty `bptools_scripts_missing_*.txt` files.
- Kept `bptools.write_questions_to_file` as a public wrapper (calling `_write_questions_to_file`) for older batch-style scripts.
- Made `bptools.add_base_args`, `bptools.add_base_args_batch`, and `bptools.default_color_wheel_calc` private (underscored); scripts should call `bptools.make_arg_parser` instead.
- Removed unused `bptools.default_color_wheel2` and `bptools.light_and_dark_color_wheel2`, and made `bptools.get_git_root` private (`_get_git_root`) since scripts should use `get_repo_data_path`.
- Added `docs/YAML_QUESTION_BANK_INDEX.md` and `tools/build_yaml_question_bank_index.py` to track YAML question bank creation/update dates (for `matching_sets/`, `problems/multiple_choice_statements/`, and `data/` YAML files).
- Added `tools/test_reorg_git_mv_commands.txt` with a suggested `tests/` subfolder re-org command list (including YAML-focused tests under `tests/yaml/`).
- Updated `tests/conftest.py` to add `tests/` to `sys.path` so helper imports (e.g., `lib_test_utils`) keep working after moving tests into subfolders.
- Made `tests/lib_test_utils.py` resolve repo paths across the `problems/` move (so tests can use legacy paths like `inheritance-problems/...` and still work).

## 2026-01-04
- Added a cytogenetic band-order question generator in
  [problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-band_order.py](problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-band_order.py).
- Added a chi-square null/alternative hypothesis question generator in
  [problems/inheritance-problems/chi_square/chi_square_hypotheses.py](problems/inheritance-problems/chi_square/chi_square_hypotheses.py).
- Added a chi-square "dumb lab partner" hypothesis mistake-spotting generator in
  [problems/inheritance-problems/chi_square/chi_square_hypotheses_lab_partner.py](problems/inheritance-problems/chi_square/chi_square_hypotheses_lab_partner.py).
- Updated both chi-square hypothesis generators to choose offspring totals that produce integer expected counts.
- Updated the phylogenetic tree batch script
  [problems/inheritance-problems/phylogenetic_trees/make_all_gene_trees.py](problems/inheritance-problems/phylogenetic_trees/make_all_gene_trees.py)
  to use [problems/inheritance-problems/phylogenetic_trees/treelib/](problems/inheritance-problems/phylogenetic_trees/treelib/) instead of `phylolib2.py`.
- Added biostatistics hypothesis-identification generators in
  [problems/biostatistics-problems/hypothesis_statements.py](problems/biostatistics-problems/hypothesis_statements.py) and
  [problems/biostatistics-problems/hypothesis_lab_partner.py](problems/biostatistics-problems/hypothesis_lab_partner.py).
- Updated [problems/biostatistics-problems/hypothesis_statements.py](problems/biostatistics-problems/hypothesis_statements.py)
  to add plain-English "In words" sentences to each option and include an ASCII-friendly parameter label in
  parentheses for improved terminal readability.
- Updated [problems/biostatistics-problems/hypothesis_lab_partner.py](problems/biostatistics-problems/hypothesis_lab_partner.py)
  to include the same ASCII-friendly parameter labels and "In words" sentences for the lab partner's hypotheses.
- Added a pytest smoke-test suite for `*lib.py` modules in [tests/](tests/) and configured pytest discovery via
  [pyproject.toml](pyproject.toml).
- Added per-library unit tests in [tests/](tests/) (one `tests/test_*.py` per `*lib.py` file) with a shared import helper
  in [tests/lib_test_utils.py](tests/lib_test_utils.py).
- Fixed [problems/biochemistry-problems/aminoacidlib.py](problems/biochemistry-problems/aminoacidlib.py) to store `sugar_code` on
  `AminoAcidStructure`, enabling structure/formula helpers to run.
- Added a dominant/X-linked recessive variation generator in
  [problems/inheritance-problems/dominant_and_X-linked_recessive_variations.py](problems/inheritance-problems/dominant_and_X-linked_recessive_variations.py)
  with varied event targets and family genotypes.
- Added a compatibility shim for `qti_package_maker` AntiCheat hidden-term insertion in
  [bptools.py](bptools.py).
- Added a monohybrid litter inference generator in
  [problems/inheritance-problems/monohybrid_litter_inference.py](problems/inheritance-problems/monohybrid_litter_inference.py)
  inspired by single-gene dominance scenarios.
- Added a lethal allele survival generator in
  [problems/inheritance-problems/lethal_allele_survival.py](problems/inheritance-problems/lethal_allele_survival.py)
  for heterozygote crosses with lethal homozygotes.
- Fixed local import resolution for Hardy-Weinberg and epistasis generators after
  directory moves, and updated Hardy-Weinberg data path resolution to use the
  repo data directory.
- Added a shared translocation helper library in
  [problems/inheritance-problems/translocation/translocationlib.py](problems/inheritance-problems/translocation/translocationlib.py)
  and refactored the Robertsonian and meiosis translocation generators to use it.
- Added new X-linked inheritance generators inspired by the 2020 practice set:
  [problems/inheritance-problems/x_linked_reciprocal_cross.py](problems/inheritance-problems/x_linked_reciprocal_cross.py)
  and [problems/inheritance-problems/x_linked_tortoiseshell.py](problems/inheritance-problems/x_linked_tortoiseshell.py).
- Added a question authoring guide based on `TEMPLATE.py` in
  [docs/QUESTION_AUTHORING_GUIDE.md](docs/QUESTION_AUTHORING_GUIDE.md).
- Added cytogenetic disorder mappings in
  [data/cytogenetic_disorders.yml](data/cytogenetic_disorders.yml).
- Added a cytogenetic disorder question generator in
  [problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-disorders.py](problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-disorders.py).
- Moved [problems/inheritance-problems/organism_data.yml](problems/inheritance-problems/organism_data.yml)
  and [problems/biostatistics-problems/student_names.txt](problems/biostatistics-problems/student_names.txt)
  into [data/](data/) and updated the generators to reference the new paths.
- Added `source_me.sh` for a repo-root `PYTHONPATH` setup and added packaging
  metadata via [pyproject.toml](pyproject.toml), [MANIFEST.in](MANIFEST.in),
  and [VERSION](VERSION) (version 26.01).
- Documented editable install behavior in
  [docs/QUESTION_AUTHORING_GUIDE.md](docs/QUESTION_AUTHORING_GUIDE.md).
- Updated [refactor-Jan_2026/upgraded_phase_1_python_scripts.txt](refactor-Jan_2026/upgraded_phase_1_python_scripts.txt)
  to use the new directory names for chi_square, cytogenetic_notation, epistasis,
  deletion_mutants, polyploid, translocation, and large_crosses.

## 2025-12-27
- Added [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md) to document repo organization.
- Added [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md) to describe major components
  and generation flow.
- Added [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md) to outline generator
  refactoring and helper adoption steps.
- Added a higher-level pedigree scenario helper in
  [problems/inheritance-problems/pedigrees/pedigree_template_gen_lib.py](problems/inheritance-problems/pedigrees/pedigree_template_gen_lib.py)
  to select inheritance-specific templates and return pedigree code strings.
- Added pedigree PNG rendering alongside HTML output in
  [problems/inheritance-problems/pedigrees/pedigree_png_lib.py](problems/inheritance-problems/pedigrees/pedigree_png_lib.py).
- Added pedigree SVG rendering alongside HTML/PNG output in
  [problems/inheritance-problems/pedigrees/pedigree_svg_lib.py](problems/inheritance-problems/pedigrees/pedigree_svg_lib.py).
- Added pedigree code validators in
  [problems/inheritance-problems/pedigrees/pedigree_validate_lib.py](problems/inheritance-problems/pedigrees/pedigree_validate_lib.py).
- Enforced minimal union partner tokens in pedigree graph specs (parents omit sex,
  inferred from known partners) and documented the rule in
  [problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Expanded pedigree graph specs to allow multiple generation-1 individuals in `F:`
  (first two define the main couple) and switched validation to treat `F:` as the
  generation-1 anchor list (outside spouses inherit generation from their partner).
- Clarified founder validation: `F:` must list partners from unions where both partners
  have unspecified parents (outside spouses paired with a child are not founders).
- Normalized union partner ordering to male-first during graph spec parsing while
  accepting either order in input specs.
- Graph spec formatter now lists founders based on parentless couples (both partners
  lack parents), avoiding over-specifying marry-in spouses in `F:`.
- CodeString rendering now preserves empty rows as `.` to keep people/connector row
  parity stable during validation and rendering.
- Adjusted pedigree layout to keep child order stable (no sorting) and removed a
  duplicate vertical-edge insertion in graph-to-code rendering.
- Restored couple placement to adjacent partner slots and added explicit midpoint
  `T` insertion for couples with children (clean `#To` patterns).
- Switched layout slots to map directly to grid columns (no *2 spacing), enabling
  true midpoint child placement and cleaner compact CodeStrings.
- Refined connector routing: midpoints only draw upward edges; child columns draw
  downward edges (eliminates `+++` bars for two-child cases).
- Updated sibship bar routing to use elbows at bar ends, yielding compact `r^d`
  patterns for two-child cases.
- Always place `T` between partners in compiled CodeStrings (even for childless
  couples) to match the standard midpoint convention.
- Pedigree pipeline improvements now yield clean minimal examples (`#To`, `r^d`)
  with stable row parity and corrected descent validation.
- Added label support for pedigrees via
  [problems/inheritance-problems/pedigrees/pedigree_label_lib.py](problems/inheritance-problems/pedigrees/pedigree_label_lib.py)
  and optional `label_string` rendering in HTML/SVG and SVG-to-PNG outputs.
- Preview generation now assigns labels by default for HTML/PNG outputs in
  [problems/inheritance-problems/pedigrees/preview_pedigree.py](problems/inheritance-problems/pedigrees/preview_pedigree.py).
- Increased SVG/PNG label font sizes for better readability in pedigree previews.
- Centered SVG/PNG label rendering (anchor-based centering with small SVG baseline
  adjustment).
- Removed the standalone PNG renderer and now convert SVG to PNG via `rsvg-convert`.
- Preview index now shows explicit SVG and PNG sections, and SVG label size was reduced.
- SVG-to-PNG conversion now flattens transparency against a white background.
- Centered couple midpoints using actual child slots to avoid skewed sibship bars.
- Added stronger colored borders around HTML (dark blue), SVG (dark red), and PNG
  (dark green) previews for clarity.
- Fixed vertical descent validation to check column-specific endpoints instead of
  flagging any connector row beneath a couple midpoint.
- Refined vertical descent validation to use per-glyph edge masks (only connectors
  with down-edges must terminate on a person).
- Added minimal valid CodeString examples to
  [problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Split pedigree tooling into focused libraries:
  [problems/inheritance-problems/pedigrees/pedigree_code_lib.py](problems/inheritance-problems/pedigrees/pedigree_code_lib.py),
  [problems/inheritance-problems/pedigrees/pedigree_html_lib.py](problems/inheritance-problems/pedigrees/pedigree_html_lib.py),
  [problems/inheritance-problems/pedigrees/pedigree_png_lib.py](problems/inheritance-problems/pedigrees/pedigree_png_lib.py).
- Removed the unused compatibility shim `problems/inheritance-problems/pedigrees/pedigree_lib.py`.
- Added inheritance mode validation in
  [problems/inheritance-problems/pedigrees/pedigree_mode_validate_lib.py](problems/inheritance-problems/pedigrees/pedigree_mode_validate_lib.py).
- Added a preview helper for HTML/PNG pedigree output in
  [problems/inheritance-problems/pedigrees/preview_pedigree.py](problems/inheritance-problems/pedigrees/preview_pedigree.py).
- Renamed pedigree template helpers for clarity:
  [problems/inheritance-problems/pedigrees/pedigree_template_gen_lib.py](problems/inheritance-problems/pedigrees/pedigree_template_gen_lib.py)
  and [problems/inheritance-problems/pedigrees/pedigree_code_templates.py](problems/inheritance-problems/pedigrees/pedigree_code_templates.py).
- Added strict CodeString validation (syntax checks plus bounding-box limits) and
  preview gating in
  [problems/inheritance-problems/pedigrees/pedigree_validate_lib.py](problems/inheritance-problems/pedigrees/pedigree_validate_lib.py)
  and [problems/inheritance-problems/pedigrees/preview_pedigree.py](problems/inheritance-problems/pedigrees/preview_pedigree.py).
- Simplified [problems/inheritance-problems/pedigrees/preview_pedigree.py](problems/inheritance-problems/pedigrees/preview_pedigree.py)
  CLI by baking in the strict validation defaults for width/height and attempts.
- Renamed pedigree question generators for clarity:
  [problems/inheritance-problems/pedigrees/write_pedigree_choice.py](problems/inheritance-problems/pedigrees/write_pedigree_choice.py) and
  [problems/inheritance-problems/pedigrees/write_pedigree_match.py](problems/inheritance-problems/pedigrees/write_pedigree_match.py).
- Added a graph-based pedigree generator in
  [problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py).
- Split graph generation concerns into
  [problems/inheritance-problems/pedigrees/pedigree_skeleton_lib.py](problems/inheritance-problems/pedigrees/pedigree_skeleton_lib.py)
  and [problems/inheritance-problems/pedigrees/pedigree_inheritance_lib.py](problems/inheritance-problems/pedigrees/pedigree_inheritance_lib.py),
  leaving `pedigree_graph_parse_lib.py` as the IR and layout helper.
- Improved pedigree layout ordering to group siblings by parent index and reduce
  long connector spans in
  [problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py).
- Added a basic three-generation layout smoke test helper in
  [problems/inheritance-problems/pedigrees/pedigree_skeleton_lib.py](problems/inheritance-problems/pedigrees/pedigree_skeleton_lib.py)
  and a small runner in
  [problems/inheritance-problems/pedigrees/layout_smoke_test.py](problems/inheritance-problems/pedigrees/layout_smoke_test.py).
- Added a simple CodeString renderer in
  [problems/inheritance-problems/pedigrees/code_render.py](problems/inheritance-problems/pedigrees/code_render.py)
  for HTML/PNG output from a provided code string.
- Extended [problems/inheritance-problems/pedigrees/code_render.py](problems/inheritance-problems/pedigrees/code_render.py)
  to support SVG output.
- Added semantic validation in
  [problems/inheritance-problems/pedigrees/code_render.py](problems/inheritance-problems/pedigrees/code_render.py)
  so invalid CodeStrings fail fast before rendering.
- Added a validation rule that vertical descent cannot terminate on a couple
  midpoint (`T`) in
  [problems/inheritance-problems/pedigrees/pedigree_validate_lib.py](problems/inheritance-problems/pedigrees/pedigree_validate_lib.py).
- Added progress logging and rejection summaries to
  [problems/inheritance-problems/pedigrees/preview_pedigree.py](problems/inheritance-problems/pedigrees/preview_pedigree.py).
- Updated [problems/inheritance-problems/pedigrees/preview_pedigree.py](problems/inheritance-problems/pedigrees/preview_pedigree.py)
  to print the graph spec and CodeString for each accepted preview.
- Documented pedigree CodeString symbols in
  [problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Documented CodeString semantics (row parity, couple/offspring encoding, and
  padding rules) in
  [problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Added row-parity semantics validation in
  [problems/inheritance-problems/pedigrees/pedigree_validate_lib.py](problems/inheritance-problems/pedigrees/pedigree_validate_lib.py).
- Tightened pedigree layout packing (component grouping and compact spacing) in
  [problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py),
  and refined row-parity semantics to allow spouse connectors on people rows.
- Centered the top-generation couple in rendered layouts by applying a column
  shift during CodeString rendering in
  [problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py).
- Implemented subtree-centered slot assignment for graph layouts in
  [problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py)
  to keep siblings contiguous and reduce long connector runs.
- Switched the graph generator to emit pedigree graph spec strings and added a
  compile step from graph spec to CodeString in
  [problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](problems/inheritance-problems/pedigrees/pedigree_graph_parse_lib.py).
- Fixed graph spec generation to emit single-letter IDs so parsing works with
  the compact graph spec grammar.
- Added a trim step in graph spec generation to cap graph size at 26 people for
  the single-letter spec format.
- Fixed generation assignment for graph specs so outside spouses inherit the
  partner generation (instead of defaulting to founders).
- Ensured single-founder previews map the founder couple to `A`/`B` so the graph
  spec begins with `F:AfBm`.
- Updated pedigree graph spec parsing/formatting so `F:` only lists generation-1
  founders (and founders cannot appear as children).
- Enforced graph spec rules: `F:` contains exactly two people (main couple),
  unions require at least one child, and sex can be inferred for outside
  spouses.
- Generator now omits childless unions when emitting graph specs to comply with
  the “couples must have children” rule.
- Clarified the internal role of PedigreeGraph in
  [problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Added a compact pedigree graph spec parser/serializer in
  [problems/inheritance-problems/pedigrees/pedigree_graph_spec_lib.py](problems/inheritance-problems/pedigrees/pedigree_graph_spec_lib.py)
  and documented the pedigree graph spec format in
  [problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Clarified in [problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md)
  that graph parsing/compilation is an internal, non-persisted step.
- Added a local pipeline note in
  [problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Expanded [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md) with decision points
  for return contracts, shortfalls, newline policy, and argparse composition.
- Added question collection helpers and shared CLI args to [bptools.py](bptools.py).
- Updated [TEMPLATE.py](TEMPLATE.py) and
  [problems/inheritance-problems/unique_cross_phenotypes.py](problems/inheritance-problems/unique_cross_phenotypes.py)
  to use the new helpers.
- Clarified helper contracts in [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md)
  to standardize `write_question(N, args)` and `write_question_batch(N, args)`.
- Added output helpers in [bptools.py](bptools.py) and updated
  [TEMPLATE.py](TEMPLATE.py) and
  [problems/inheritance-problems/unique_cross_phenotypes.py](problems/inheritance-problems/unique_cross_phenotypes.py)
  to use the combined collection+write flow.
- Updated `make_outfile` to default to `sys.argv[0]` so scripts can omit `__file__`.
- Added `--duplicate-runs` as the preferred long flag (with `--duplicates` as an alias)
  in [bptools.py](bptools.py), and documented it in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Added standard argparse bundles `add_choice_args` and `add_hint_args` in
  [bptools.py](bptools.py) and documented them in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Added standard argparse bundles `add_question_format_args` and
  `add_difficulty_args` in [bptools.py](bptools.py) and documented them in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Updated `add_question_format_args` to accept a list of formats and only add
  flags for the requested types.
- Updated `problems/inheritance-problems/unique_cross_genotypes.py`,
  `problems/inheritance-problems/unique_cross_phenotypes.py`, and
  `problems/inheritance-problems/unique_gametes.py` to use the new helper system.
- Removed single-letter question format flags from `add_question_format_args` and
  added long-form aliases like `--multiple-choice` and `--fill-in-blank`.
- Updated `bptools.print_histogram()` to use `tabulate` with `fancy_grid` output.
- Updated `bptools.print_histogram()` to render choices as columns with a final
  TOTAL column.
- Fixed indentation in `problems/inheritance-problems/unique_gametes.py`.
- Updated `problems/biochemistry-problems/ionic_bond_amino_acids.py`,
  `problems/biochemistry-problems/macromolecules_categorize_by_name.py`, and
  `problems/biochemistry-problems/alpha_helix_h-bonds.py` to use shared helpers and
  standardized argparse bundles.
- Standardized `add_base_args` defaults to `duplicate_runs=2` and no max question
  cap by default.
- Fixed `problems/biochemistry-problems/ionic_bond_amino_acids.py` to honor `--num-choices`.
- Set a default `max_questions` cap for batch output in
  `problems/biochemistry-problems/macromolecules_categorize_by_name.py`.
- Added `add_base_args_batch()` in [bptools.py](bptools.py) and switched
  `problems/biochemistry-problems/macromolecules_categorize_by_name.py` to use it.
- Added `make_arg_parser()` in [bptools.py](bptools.py) and updated scripts to
  use it for consistent parser defaults.
- Switched `problems/inheritance-problems/unique_cross_genotypes.py` and
  `problems/inheritance-problems/unique_cross_phenotypes.py` to `make_arg_parser()`.
- Added `tabulate` to [pip_requirements.txt](pip_requirements.txt).
- Refactored [problems/dna_profiling-problems/hla_genotype.py](problems/dna_profiling-problems/hla_genotype.py)
  to use standard argparse helpers and `collect_and_write_questions`.
- Refactored [problems/cell_biology-problems/cell_surf-to-vol_ratio.py](problems/cell_biology-problems/cell_surf-to-vol_ratio.py)
  to use standard argparse helpers and `collect_and_write_questions`.
- Refactored [problems/laboratory-problems/vol-vol_solution_numeric.py](problems/laboratory-problems/vol-vol_solution_numeric.py)
  to use batch helpers and rely on `-d/--duplicate-runs` for per-liquid repeats.
- Added a legacy-modernization checklist section to
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored [problems/biostatistics-problems/descriptive_stats_google_sheet.py](problems/biostatistics-problems/descriptive_stats_google_sheet.py)
  to use shared argparse and helper-driven question collection.
- Refactored [problems/molecular_biology-problems/consensus_sequence_MC.py](problems/molecular_biology-problems/consensus_sequence_MC.py)
  to use shared helpers, standardized args, and Blackboard MC formatting.
- Refactored [problems/inheritance-problems/dihybrid_cross_epistatic_gene_interactions.py](problems/inheritance-problems/dihybrid_cross_epistatic_gene_interactions.py)
  to use shared helpers and standardized args.
- Fixed prime-mode complementary sequence answers to use reverse complements and
  consistent 5'->3' display in
  [problems/molecular_biology-problems/complementary_sequences.py](problems/molecular_biology-problems/complementary_sequences.py).
- Added `reverse_complement()` to
  [problems/molecular_biology-problems/seqlib.py](problems/molecular_biology-problems/seqlib.py).
- Added an answer check script at
  [tests/check_complementary_sequences_prime.py](tests/check_complementary_sequences_prime.py).
- Refactored [problems/molecular_biology-problems/complementary_sequences.py](problems/molecular_biology-problems/complementary_sequences.py)
  to use the shared argparse and helper workflow.
- Updated `complementary_sequences.py` to use `-d/--duplicate-runs` and
  `-x/--max-questions` instead of a custom `--num-sequences` argument.
- Added inline HTML style presets in
  [problems/molecular_biology-problems/seqlib.py](problems/molecular_biology-problems/seqlib.py)
  for consistent table borders and monospace cells.
- Added simple assertion tests for core helpers in
  [problems/molecular_biology-problems/seqlib.py](problems/molecular_biology-problems/seqlib.py).
- Added short descriptions for all `*lib.py` modules in
  [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md).
- Added [docs/TODO.md](docs/TODO.md) to track backlog items (including a possible
  `make_outfile_from_args()` helper).
- Refactored [problems/biochemistry-problems/quick_fatty_acid_colon_system.py](problems/biochemistry-problems/quick_fatty_acid_colon_system.py)
  to use batch helpers and `bptools` formatting.
- Refactored [problems/inheritance-problems/cytogenetic_notation-aneuploidy.py](problems/inheritance-problems/cytogenetic_notation-aneuploidy.py)
  to use shared argparse, question helpers, and unified output handling.
- Refactored [problems/laboratory-problems/serial_dilution_factor_mc.py](problems/laboratory-problems/serial_dilution_factor_mc.py)
  to use batch helpers and a computed default duplicate count.
- Added migration notes for batch upgrades in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored [problems/molecular_biology-problems/rna_transcribe_fill_blank.py](problems/molecular_biology-problems/rna_transcribe_fill_blank.py)
  to use shared argparse helpers and question collection.
- Kept [problems/biostatistics-problems/make_html_box_plot.py](problems/biostatistics-problems/make_html_box_plot.py)
  as a helper-only HTML utility (not a question generator).
- Refactored [problems/laboratory-problems/serial_dilution_factor_diluent_numeric.py](problems/laboratory-problems/serial_dilution_factor_diluent_numeric.py)
  to use batch helpers and a computed default duplicate count.
- Added a migration note for raw HTML emitters in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored [problems/laboratory-problems/percent_dilution_aliquot_numeric.py](problems/laboratory-problems/percent_dilution_aliquot_numeric.py)
  to use batch helpers and a fixed default duplicate count.
- Fixed an HTML paragraph nesting error in
  [problems/laboratory-problems/percent_dilution_aliquot_numeric.py](problems/laboratory-problems/percent_dilution_aliquot_numeric.py).
- Refactored [problems/inheritance-problems/blood_type_offspring.py](problems/inheritance-problems/blood_type_offspring.py)
  to use batch helpers with a shared parser and outfile builder.
- Refactored [problems/inheritance-problems/probabiliy_of_progeny.py](problems/inheritance-problems/probabiliy_of_progeny.py)
  to use shared argparse defaults and helper-based question collection.
- Refactored [problems/inheritance-problems/chisquare/chi_square_errors.py](problems/inheritance-problems/chisquare/chi_square_errors.py)
  to use shared argparse defaults and helper-based question collection.
- Added a migration note for fixed-grid batch scripts in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Converted laboratory generators from batch to per-question writers (Option 2
  selection) in:
  [problems/laboratory-problems/mass_solution_numeric.py](problems/laboratory-problems/mass_solution_numeric.py),
  [problems/laboratory-problems/orders_of_magnitude_mc.py](problems/laboratory-problems/orders_of_magnitude_mc.py),
  [problems/laboratory-problems/percent_dilution_aliquot_numeric.py](problems/laboratory-problems/percent_dilution_aliquot_numeric.py),
  [problems/laboratory-problems/pipet_size_mc.py](problems/laboratory-problems/pipet_size_mc.py),
  [problems/laboratory-problems/serial_dilution_factor_diluent_numeric.py](problems/laboratory-problems/serial_dilution_factor_diluent_numeric.py),
  [problems/laboratory-problems/serial_dilution_factor_mc.py](problems/laboratory-problems/serial_dilution_factor_mc.py),
  [problems/laboratory-problems/vol-vol_solution_numeric.py](problems/laboratory-problems/vol-vol_solution_numeric.py),
  [problems/laboratory-problems/weight-vol_solution_numeric.py](problems/laboratory-problems/weight-vol_solution_numeric.py).
- Added monospace formatting for numeric volumes/units across laboratory question
  text and choices (including dilution factor, percent dilution, mass/volume,
  molar solution, pipet, and serial dilution scripts).
- Removed unused [logger_config.py](logger_config.py).
- Fixed HTML quoting in [problems/molecular_biology-problems/seqlib.py](problems/molecular_biology-problems/seqlib.py)
  to avoid invalid inline style attributes.
- Added max-questions early-stop handling in
  [problems/molecular_biology-problems/overhang_type.py](problems/molecular_biology-problems/overhang_type.py).
- Fixed malformed HTML attributes in
  [problems/molecular_biology-problems/enhancer_gene_expression.py](problems/molecular_biology-problems/enhancer_gene_expression.py).
- Fixed paragraph nesting in
  [problems/inheritance-problems/chisquare/chi_square_hardy_weinberg.py](problems/inheritance-problems/chisquare/chi_square_hardy_weinberg.py).
- Implemented missing choice generation in
  [problems/inheritance-problems/cytogenetic_notation-sub-band_notation.py](problems/inheritance-problems/cytogenetic_notation-sub-band_notation.py).
- Fixed HTML entity formatting in
  [problems/biochemistry-problems/fatty_acid_naming.py](problems/biochemistry-problems/fatty_acid_naming.py).
- Fixed HTML paragraph closure in
  [problems/molecular_biology-problems/rna_transcribe_prime_fill_blank.py](problems/molecular_biology-problems/rna_transcribe_prime_fill_blank.py).
- Quoted HTML attribute values in
  [problems/molecular_biology-problems/exon_splicing.py](problems/molecular_biology-problems/exon_splicing.py)
  to satisfy XML parsing.
- Corrected outfile suffix selection in
  [problems/inheritance-problems/hardy_weinberg_numeric.py](problems/inheritance-problems/hardy_weinberg_numeric.py).
- Added max-questions early-stop handling in
  [problems/inheritance-problems/pedigrees/write_pedigree_match.py](problems/inheritance-problems/pedigrees/write_pedigree_match.py).
- Improved dilution factor MC choices and formatting (clarified labels, background
  explanation, colored aliquot/diluent with monospace values, and standardized
  `--num-choices`) in
  [problems/laboratory-problems/dilution_factor_mc.py](problems/laboratory-problems/dilution_factor_mc.py).
- De-duplicated numeric pH choices to avoid repeated labels in
  [problems/biochemistry-problems/buffers/optimal_buffering_range.py](problems/biochemistry-problems/buffers/optimal_buffering_range.py).
- Cleaned unused imports and a redundant global in [bptools.py](bptools.py) to
  satisfy pyflakes.
- Fixed a pyflakes warning in
  [problems/biochemistry-problems/buffers/bufferslib.py](problems/biochemistry-problems/buffers/bufferslib.py)
  by validating pKa values without unused variables.
- Fixed a bad error message variable in
  [problems/biochemistry-problems/carbohydrates_classification/sugarlib.py](problems/biochemistry-problems/carbohydrates_classification/sugarlib.py).
- Removed an unused import and a bad escape sequence in
  [problems/biochemistry-problems/aminoacidlib.py](problems/biochemistry-problems/aminoacidlib.py).
- Removed unused imports/vars in
  [problems/biochemistry-problems/proteinlib.py](problems/biochemistry-problems/proteinlib.py) and
  [problems/dna_profiling-problems/gellib.py](problems/dna_profiling-problems/gellib.py).
- Refactored [problems/laboratory-problems/dilution_factor_calc_numeric.py](problems/laboratory-problems/dilution_factor_calc_numeric.py)
  to use shared argparse defaults and helper-based question collection.
- Refactored [problems/biochemistry-problems/which_lipid-chemical_formula.py](problems/biochemistry-problems/which_lipid-chemical_formula.py)
  to use `bptools` MC formatting and shared helpers instead of manual text output.
- Refactored [problems/inheritance-problems/dihybrid_cross_epistatic_gene_metabolics.py](problems/inheritance-problems/dihybrid_cross_epistatic_gene_metabolics.py)
  to use shared argparse defaults, helper-based question collection, and remove
  debug prints.
- Added a migration note about preserving cyclic scenario selection in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored [problems/biochemistry-problems/buffers/pKa_buffer_state.py](problems/biochemistry-problems/buffers/pKa_buffer_state.py)
  to use batch helpers and a shared parser while preserving proton-count logic.
- Refactored [problems/inheritance-problems/poisson_flies.py](problems/inheritance-problems/poisson_flies.py)
  to use shared argparse defaults and helper-based question collection.
- Refactored [problems/biochemistry-problems/chymotrypsin_substrate.py](problems/biochemistry-problems/chymotrypsin_substrate.py)
  to use shared helpers, and moved the `--max-length` short flag from `-x` to `-M`
  to avoid conflict with `-x/--max-questions`.
- Updated [problems/biochemistry-problems/chymotrypsin_substrate.py](problems/biochemistry-problems/chymotrypsin_substrate.py)
  to map RasMol families to the custom palette, keep RasMol for the “weird”
  residues, and darken gray residues for white backgrounds.
- Added a migration note about `-x` short-flag conflicts in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Simplified `bptools.add_choice_args()` to a fixed API with a single `default=`
  parameter, and updated scripts to use that form.
- Set `problems/biochemistry-problems/alpha_helix_h-bonds.py` to use
  `add_choice_args(..., default=4)`.
- Added `bptools.get_repo_data_path()` and switched
  `problems/biochemistry-problems/isoelectric_two_proteins.py` to use it for data file
  resolution.
- Switched `problems/biochemistry-problems/isoelectric_one_protein.py`,
  `problems/biochemistry-problems/carbohydrates_classification/sugarlib.py`,
  `problems/biochemistry-problems/proteinlib.py`, and `problems/inheritance-problems/disorderlib.py`
  to use `bptools.get_repo_data_path()` for data file resolution.
- Switched `problems/biochemistry-problems/PUBCHEM/wordle_peptides.py` and
  `problems/inheritance-problems/deletion_mutant_words.py` to use
  `bptools.get_repo_data_path()` for data file resolution, and removed the
  local `get_git_root()` helper from
  `problems/biochemistry-problems/carbohydrates_classification/sugarlib.py`.
- Refactored [problems/biochemistry-problems/isoelectric_two_proteins.py](problems/biochemistry-problems/isoelectric_two_proteins.py)
  to use shared argparse defaults, cached protein data, and helper-based output.
- Refactored [problems/inheritance-problems/epistasis_test_cross.py](problems/inheritance-problems/epistasis_test_cross.py)
  to use shared argparse defaults, helper-based question collection, and
  standardized outfile naming.
- Refactored [problems/molecular_biology-problems/mutant_screen.py](problems/molecular_biology-problems/mutant_screen.py)
  to use shared argparse defaults, MC/FIB format flags, and helper-based output.
- Fixed the mutant screen HTML table to quote the width attribute for valid XML
  in [problems/molecular_biology-problems/mutant_screen.py](problems/molecular_biology-problems/mutant_screen.py).
- Refactored [problems/molecular_biology-problems/pcr_design.py](problems/molecular_biology-problems/pcr_design.py)
  to use shared argparse defaults and helper-based MC formatting.
- Refactored [problems/inheritance-problems/polyploid-monoploid_v_haploid.py](problems/inheritance-problems/polyploid-monoploid_v_haploid.py)
  to use batch helpers and shared argparse defaults.
- Refactored [problems/laboratory-problems/serial_dilution_factor_aliquot_numeric.py](problems/laboratory-problems/serial_dilution_factor_aliquot_numeric.py)
  to use batch helpers and a computed default duplicate count.
- Added a migration note about preserving computed duplicate defaults for batch
  scripts in [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Switched [problems/inheritance-problems/polyploid-monoploid_v_haploid.py](problems/inheritance-problems/polyploid-monoploid_v_haploid.py)
  and [problems/laboratory-problems/serial_dilution_factor_aliquot_numeric.py](problems/laboratory-problems/serial_dilution_factor_aliquot_numeric.py)
  to non-batch question generation with scenario selection modes.
- Set the default duplicates for
  [problems/laboratory-problems/serial_dilution_factor_aliquot_numeric.py](problems/laboratory-problems/serial_dilution_factor_aliquot_numeric.py)
  back to 2 for quick testing.
- Removed per-script `duplicates_default` overrides so scripts consistently use
  the shared default of 2 (including buffers, percent dilution, and serial
  dilution variants).
- Removed `duplicates_default` override support from `bptools.add_base_args`,
  `add_base_args_batch`, and `make_arg_parser`, keeping a fixed default of 2.
- Removed `max_questions_default` override support from `bptools` parser helpers,
  keeping a fixed default of None for single-question scripts and 99 for batch.
- Documented how to switch batch scripts from fixed cycles to individual
  scenario selection in [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Added a migration note about converting stdout-based question scripts to
  helper-based MC/FIB formatting in [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored [problems/molecular_biology-problems/overhang_sequence.py](problems/molecular_biology-problems/overhang_sequence.py)
  to use batch helpers, shared argparse defaults, and unified outfile naming.
- Refactored [problems/inheritance-problems/pedigrees/write_pedigree_match.py](problems/inheritance-problems/pedigrees/write_pedigree_match.py)
  to use batch helpers and start-numbered matching sets.
- Refactored [problems/biochemistry-problems/Henderson-Hasselbalch.py](problems/biochemistry-problems/Henderson-Hasselbalch.py)
  to use shared argparse defaults and helper-based question collection.
- Added a migration note about start-numbering for batch-generated lists in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Set defaults for question format/direction in
  [problems/molecular_biology-problems/complementary_sequences.py](problems/molecular_biology-problems/complementary_sequences.py)
  and [problems/inheritance-problems/epistasis_test_cross.py](problems/inheritance-problems/epistasis_test_cross.py)
  so they run without required flags.
- Set default question formats in
  [problems/molecular_biology-problems/overhang_sequence.py](problems/molecular_biology-problems/overhang_sequence.py)
  and [problems/biochemistry-problems/Henderson-Hasselbalch.py](problems/biochemistry-problems/Henderson-Hasselbalch.py)
  so they run without required flags.
- Set defaults for `alpha_helix_h-bonds.py` question type and
  `pKa_buffer_state.py` proton count, and fixed the overhang script to use the
  `question_type` dest so it runs without required flags.
- Fixed `add_question_format_args()` to always use `question_type` and updated
  callers (`complementary_sequences`, `overhang_sequence`, `alpha_helix_h-bonds`,
  `mutant_screen`, and `TEMPLATE.py`) to stop overriding dest.
- Fixed an indentation error in
  [problems/biochemistry-problems/alpha_helix_h-bonds.py](problems/biochemistry-problems/alpha_helix_h-bonds.py).
- Fixed duplicate argparse base-arg registration in
  [problems/inheritance-problems/unique_gametes.py](problems/inheritance-problems/unique_gametes.py).
- Added a max-questions early-exit check to
  [problems/molecular_biology-problems/overhang_sequence.py](problems/molecular_biology-problems/overhang_sequence.py)
  to avoid long full-list runs when `-x` is set.
- Refactored [problems/laboratory-problems/molar_solution_using_mw_numeric.py](problems/laboratory-problems/molar_solution_using_mw_numeric.py)
  to use shared argparse defaults and helper-based question collection.
- Refactored [problems/molecular_biology-problems/translate_genetic_code.py](problems/molecular_biology-problems/translate_genetic_code.py)
  to use shared argparse defaults, cached data reads, and helper-based question collection.
- Refactored [problems/biochemistry-problems/fret_overlap_colors.py](problems/biochemistry-problems/fret_overlap_colors.py)
  to use shared argparse defaults, MC formatting helpers, and randomized question selection.
- Added migration notes about replacing custom `-q/--num-questions` flags and
  about using repo data helpers in [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored biochemistry scripts to use shared argparse defaults and helper-based
  question collection:
  [problems/biochemistry-problems/buffers/optimal_buffering_range.py](problems/biochemistry-problems/buffers/optimal_buffering_range.py),
  [problems/biochemistry-problems/fatty_acid_naming.py](problems/biochemistry-problems/fatty_acid_naming.py),
  [problems/biochemistry-problems/fret_permute_colors.py](problems/biochemistry-problems/fret_permute_colors.py),
  [problems/biochemistry-problems/isoelectric_one_protein.py](problems/biochemistry-problems/isoelectric_one_protein.py),
  [problems/biochemistry-problems/metabolic_pathway_allosteric.py](problems/biochemistry-problems/metabolic_pathway_allosteric.py),
  [problems/biochemistry-problems/metabolic_pathway_inhibitor.py](problems/biochemistry-problems/metabolic_pathway_inhibitor.py),
  [problems/biochemistry-problems/michaelis_menten_table-inhibition.py](problems/biochemistry-problems/michaelis_menten_table-inhibition.py),
  [problems/biochemistry-problems/michaelis_menten_table-Km.py](problems/biochemistry-problems/michaelis_menten_table-Km.py),
  [problems/biochemistry-problems/optimal_enzyme-type_1.py](problems/biochemistry-problems/optimal_enzyme-type_1.py),
  [problems/biochemistry-problems/optimal_enzyme-type_2.py](problems/biochemistry-problems/optimal_enzyme-type_2.py),
  [problems/biochemistry-problems/optimal_enzyme-type_3.py](problems/biochemistry-problems/optimal_enzyme-type_3.py),
  [problems/biochemistry-problems/photosynthetic_light_pigments.py](problems/biochemistry-problems/photosynthetic_light_pigments.py),
  [problems/biochemistry-problems/protein_gel_migration.py](problems/biochemistry-problems/protein_gel_migration.py),
  [problems/biochemistry-problems/which_hydrophobic-simple.py](problems/biochemistry-problems/which_hydrophobic-simple.py).
- Refactored biostatistics scripts to use shared argparse defaults and helper-based
  question collection:
  [problems/biostatistics-problems/babies_two_sample_t_test.py](problems/biostatistics-problems/babies_two_sample_t_test.py),
  [problems/biostatistics-problems/busse_woods_one_sample_tests.py](problems/biostatistics-problems/busse_woods_one_sample_tests.py),
  [problems/biostatistics-problems/busse_woods_two_sample_t_test.py](problems/biostatistics-problems/busse_woods_two_sample_t_test.py),
  [problems/biostatistics-problems/population_test_google_sheet.py](problems/biostatistics-problems/population_test_google_sheet.py),
  [problems/biostatistics-problems/z_score_google_sheet.py](problems/biostatistics-problems/z_score_google_sheet.py),
  [problems/biostatistics-problems/z_score_table_interp.py](problems/biostatistics-problems/z_score_table_interp.py).
- Refactored DNA profiling scripts to use shared argparse defaults, helper-based
  question collection, and parameter wrappers:
  [problems/dna_profiling-problems/blood_type_agglutination_test.py](problems/dna_profiling-problems/blood_type_agglutination_test.py),
  [problems/dna_profiling-problems/who_father_html.py](problems/dna_profiling-problems/who_father_html.py),
  [problems/dna_profiling-problems/who_killer_html.py](problems/dna_profiling-problems/who_killer_html.py).
- Refactored inheritance scripts to use shared argparse defaults and helper-based
  question collection or batch helpers:
  [problems/inheritance-problems/blood_type_mother.py](problems/inheritance-problems/blood_type_mother.py),
  [problems/inheritance-problems/chisquare/chi_square_calculated.py](problems/inheritance-problems/chisquare/chi_square_calculated.py),
  [problems/inheritance-problems/chisquare/chi_square_choices.py](problems/inheritance-problems/chisquare/chi_square_choices.py),
  [problems/inheritance-problems/chisquare/chi_square_hardy_weinberg.py](problems/inheritance-problems/chisquare/chi_square_hardy_weinberg.py),
  [problems/inheritance-problems/cytogenetic_notation-rearrangements.py](problems/inheritance-problems/cytogenetic_notation-rearrangements.py),
  [problems/inheritance-problems/cytogenetic_notation-sub-band_notation.py](problems/inheritance-problems/cytogenetic_notation-sub-band_notation.py),
  [problems/inheritance-problems/deletion_mutant_random.py](problems/inheritance-problems/deletion_mutant_random.py),
  [problems/inheritance-problems/deletion_mutant_words.py](problems/inheritance-problems/deletion_mutant_words.py),
  [problems/inheritance-problems/dominant_and_X-linked_recessive.py](problems/inheritance-problems/dominant_and_X-linked_recessive.py),
  [problems/inheritance-problems/hardy_weinberg_mc_type.py](problems/inheritance-problems/hardy_weinberg_mc_type.py),
  [problems/inheritance-problems/hardy_weinberg_numeric.py](problems/inheritance-problems/hardy_weinberg_numeric.py),
  [problems/inheritance-problems/horses.py](problems/inheritance-problems/horses.py),
  [problems/inheritance-problems/letter_translocation_problem_color.py](problems/inheritance-problems/letter_translocation_problem_color.py),
  [problems/inheritance-problems/monohybrid_degrees_of_dominance.py](problems/inheritance-problems/monohybrid_degrees_of_dominance.py),
  [problems/inheritance-problems/monohybrid_genotype_statements.py](problems/inheritance-problems/monohybrid_genotype_statements.py),
  [problems/inheritance-problems/old_deletion_mutants.py](problems/inheritance-problems/old_deletion_mutants.py),
  [problems/inheritance-problems/pedigrees/write_pedigree_choice.py](problems/inheritance-problems/pedigrees/write_pedigree_choice.py),
  [problems/inheritance-problems/polyploid-gametes.py](problems/inheritance-problems/polyploid-gametes.py),
  [problems/inheritance-problems/punnett_choice.py](problems/inheritance-problems/punnett_choice.py),
  [problems/inheritance-problems/robertsonian.py](problems/inheritance-problems/robertsonian.py),
  [problems/inheritance-problems/translocation_meiosis_table.py](problems/inheritance-problems/translocation_meiosis_table.py).
- Refactored laboratory scripts to use shared argparse defaults and helper-based
  question collection:
  [problems/laboratory-problems/dilution_factor_aliquot_numeric.py](problems/laboratory-problems/dilution_factor_aliquot_numeric.py),
  [problems/laboratory-problems/dilution_factor_diluent_numeric.py](problems/laboratory-problems/dilution_factor_diluent_numeric.py),
  [problems/laboratory-problems/dilution_factor_mc.py](problems/laboratory-problems/dilution_factor_mc.py),
  [problems/laboratory-problems/mass_solution_numeric.py](problems/laboratory-problems/mass_solution_numeric.py),
  [problems/laboratory-problems/orders_of_magnitude_mc.py](problems/laboratory-problems/orders_of_magnitude_mc.py),
  [problems/laboratory-problems/pipet_size_mc.py](problems/laboratory-problems/pipet_size_mc.py),
  [problems/laboratory-problems/weight-vol_solution_numeric.py](problems/laboratory-problems/weight-vol_solution_numeric.py).
- Refactored molecular biology scripts to use shared argparse defaults and helper-based
  question collection:
  [problems/molecular_biology-problems/amplicon_copies.py](problems/molecular_biology-problems/amplicon_copies.py),
  [problems/molecular_biology-problems/beadle_tatum-metabolic_pathway.py](problems/molecular_biology-problems/beadle_tatum-metabolic_pathway.py),
  [problems/molecular_biology-problems/chargaff_dna_percent.py](problems/molecular_biology-problems/chargaff_dna_percent.py),
  [problems/molecular_biology-problems/consensus_sequence_FIB-arbitrary_code.py](problems/molecular_biology-problems/consensus_sequence_FIB-arbitrary_code.py),
  [problems/molecular_biology-problems/consensus_sequence_FIB-easy.py](problems/molecular_biology-problems/consensus_sequence_FIB-easy.py),
  [problems/molecular_biology-problems/consensus_sequence_FIB-hard.py](problems/molecular_biology-problems/consensus_sequence_FIB-hard.py),
  [problems/molecular_biology-problems/dna_gel-closest_farthest_MC.py](problems/molecular_biology-problems/dna_gel-closest_farthest_MC.py),
  [problems/molecular_biology-problems/dna_gel-estimate_size-MC_or_NUM.py](problems/molecular_biology-problems/dna_gel-estimate_size-MC_or_NUM.py),
  [problems/molecular_biology-problems/dna_melting_temp.py](problems/molecular_biology-problems/dna_melting_temp.py),
  [problems/molecular_biology-problems/enhancer_gene_expression.py](problems/molecular_biology-problems/enhancer_gene_expression.py),
  [problems/molecular_biology-problems/exon_splicing.py](problems/molecular_biology-problems/exon_splicing.py),
  [problems/molecular_biology-problems/inverse_pcr_design.py](problems/molecular_biology-problems/inverse_pcr_design.py),
  [problems/molecular_biology-problems/linear_digest.py](problems/molecular_biology-problems/linear_digest.py),
  [problems/molecular_biology-problems/nested_pcr_design.py](problems/molecular_biology-problems/nested_pcr_design.py),
  [problems/molecular_biology-problems/overhang_type.py](problems/molecular_biology-problems/overhang_type.py),
  [problems/molecular_biology-problems/palindrome_sequence_match.py](problems/molecular_biology-problems/palindrome_sequence_match.py),
  [problems/molecular_biology-problems/rna_transcribe_prime_fill_blank.py](problems/molecular_biology-problems/rna_transcribe_prime_fill_blank.py),
  [problems/molecular_biology-problems/rna_transcribe_prime.py](problems/molecular_biology-problems/rna_transcribe_prime.py),
  [problems/molecular_biology-problems/RT-qPCR.py](problems/molecular_biology-problems/RT-qPCR.py).
- Implemented a working RT-qPCR numeric generator in
  [problems/molecular_biology-problems/RT-qPCR.py](problems/molecular_biology-problems/RT-qPCR.py),
  including randomized Ct tables and fold-change calculations.
- Added difficulty presets for parameter-heavy restriction digest generation in
  [problems/molecular_biology-problems/linear_digest.py](problems/molecular_biology-problems/linear_digest.py).
- Added difficulty presets for parameter-heavy generators:
  [problems/molecular_biology-problems/nested_pcr_design.py](problems/molecular_biology-problems/nested_pcr_design.py),
  [problems/inheritance-problems/deletion_mutant_words.py](problems/inheritance-problems/deletion_mutant_words.py),
  [problems/inheritance-problems/deletion_mutant_random.py](problems/inheritance-problems/deletion_mutant_random.py),
  [problems/dna_profiling-problems/hla_genotype.py](problems/dna_profiling-problems/hla_genotype.py),
  [problems/biochemistry-problems/PUBCHEM/polypeptide_mc_sequence.py](problems/biochemistry-problems/PUBCHEM/polypeptide_mc_sequence.py).
- Removed non-generator utilities from the phase-1 upgrade list and tracked them
  as utilities instead: 
  [problems/inheritance-problems/pedigrees/pedigree_code_templates.py](problems/inheritance-problems/pedigrees/pedigree_code_templates.py),
  [problems/inheritance-problems/population_logistic_map_chaos.py](problems/inheritance-problems/population_logistic_map_chaos.py).
- Updated biostatistics box plot generators to use Tukey hinges, allow ties, and
  replace numeric nudges with misconception-based distractors:
  [problems/biostatistics-problems/boxplot_from_sorted_data.py](problems/biostatistics-problems/boxplot_from_sorted_data.py),
  [problems/biostatistics-problems/boxplot_from_unsorted_even.py](problems/biostatistics-problems/boxplot_from_unsorted_even.py),
  [problems/biostatistics-problems/boxplot_from_summary.py](problems/biostatistics-problems/boxplot_from_summary.py),
  [problems/biostatistics-problems/boxplot_from_cdf.py](problems/biostatistics-problems/boxplot_from_cdf.py).
- Allowed nondecreasing summaries and fractional quartiles in box plot rendering:
  [problems/biostatistics-problems/make_html_box_plot.py](problems/biostatistics-problems/make_html_box_plot.py).
- Updated box plot tests for Tukey hinges, ties, and fractional quartiles:
  [tests/libs/biostatistics/test_biostatistics_boxplots.py](tests/libs/biostatistics/test_biostatistics_boxplots.py).
- Added shared box plot helpers to reduce duplication in biostatistics generators:
  [problems/biostatistics-problems/box_plot_lib.py](problems/biostatistics-problems/box_plot_lib.py).
- Added dedicated box plot library tests:
  [tests/libs/biostatistics/test_box_plot_lib.py](tests/libs/biostatistics/test_box_plot_lib.py).
- Updated carbohydrate sugar code loading to use the repo data directory helper:
  [problems/biochemistry-problems/carbohydrates_classification/sugarlib.py](problems/biochemistry-problems/carbohydrates_classification/sugarlib.py).
- Replaced sys.exit calls in Haworth projection generation with exceptions:
  [problems/biochemistry-problems/carbohydrates_classification/sugarlib.py](problems/biochemistry-problems/carbohydrates_classification/sugarlib.py).
- Reused a single SugarCodes instance per generator run to avoid repeated YAML loads:
  [problems/biochemistry-problems/carbohydrates_classification/classify_Fischer.py](problems/biochemistry-problems/carbohydrates_classification/classify_Fischer.py),
  [problems/biochemistry-problems/carbohydrates_classification/classify_Haworth.py](problems/biochemistry-problems/carbohydrates_classification/classify_Haworth.py).
- Guarded Haworth projection generators against None returns from invalid ring sizes:
  [problems/biochemistry-problems/carbohydrates_classification/classify_Haworth.py](problems/biochemistry-problems/carbohydrates_classification/classify_Haworth.py),
  [problems/biochemistry-problems/carbohydrates_classification/convert_Haworth_to_Fischer.py](problems/biochemistry-problems/carbohydrates_classification/convert_Haworth_to_Fischer.py),
  [problems/biochemistry-problems/carbohydrates_classification/convert_Fischer_to_Haworth.py](problems/biochemistry-problems/carbohydrates_classification/convert_Fischer_to_Haworth.py),
  [problems/biochemistry-problems/carbohydrates_classification/D_to_L_Haworth_configuration.py](problems/biochemistry-problems/carbohydrates_classification/D_to_L_Haworth_configuration.py).
- Fixed arabinose spelling in sugar code data:
  [data/sugar_codes.yml](data/sugar_codes.yml).
- Migrated carbohydrate classification generators to the standard question framework:
  [problems/biochemistry-problems/carbohydrates_classification/D_to_L_Fischer_configuration.py](problems/biochemistry-problems/carbohydrates_classification/D_to_L_Fischer_configuration.py),
  [problems/biochemistry-problems/carbohydrates_classification/D_to_L_Haworth_configuration.py](problems/biochemistry-problems/carbohydrates_classification/D_to_L_Haworth_configuration.py),
  [problems/biochemistry-problems/carbohydrates_classification/classify_Fischer.py](problems/biochemistry-problems/carbohydrates_classification/classify_Fischer.py),
  [problems/biochemistry-problems/carbohydrates_classification/classify_Haworth.py](problems/biochemistry-problems/carbohydrates_classification/classify_Haworth.py).
- Dropped CLI choice-count overrides for fixed-choice carbohydrate classification items:
  [problems/biochemistry-problems/carbohydrates_classification/classify_Fischer.py](problems/biochemistry-problems/carbohydrates_classification/classify_Fischer.py),
  [problems/biochemistry-problems/carbohydrates_classification/classify_Haworth.py](problems/biochemistry-problems/carbohydrates_classification/classify_Haworth.py).
- Added coverage for SugarCodes filters, enantiomer mapping, flip behavior, and formula output:
  [tests/libs/test_biochemistry_sugarlib.py](tests/libs/test_biochemistry_sugarlib.py).
- Fixed ketoheptose comment in Haworth ring selection logic:
  [problems/biochemistry-problems/carbohydrates_classification/D_to_L_Haworth_configuration.py](problems/biochemistry-problems/carbohydrates_classification/D_to_L_Haworth_configuration.py),
  [problems/biochemistry-problems/carbohydrates_classification/convert_Haworth_to_Fischer.py](problems/biochemistry-problems/carbohydrates_classification/convert_Haworth_to_Fischer.py),
  [problems/biochemistry-problems/carbohydrates_classification/convert_Fischer_to_Haworth.py](problems/biochemistry-problems/carbohydrates_classification/convert_Fischer_to_Haworth.py).
- Migrated Haworth/Fischer conversion generators to the standard question framework:
  [problems/biochemistry-problems/carbohydrates_classification/convert_Haworth_to_Fischer.py](problems/biochemistry-problems/carbohydrates_classification/convert_Haworth_to_Fischer.py),
  [problems/biochemistry-problems/carbohydrates_classification/convert_Fischer_to_Haworth.py](problems/biochemistry-problems/carbohydrates_classification/convert_Fischer_to_Haworth.py).
- Migrated two-point test cross gene mapping generators to the standard question framework:
  [problems/inheritance-problems/gene_mapping/two-point_test_cross-cis-trans.py](problems/inheritance-problems/gene_mapping/two-point_test_cross-cis-trans.py),
  [problems/inheritance-problems/gene_mapping/two-point_test_cross-distance.py](problems/inheritance-problems/gene_mapping/two-point_test_cross-distance.py),
  [problems/inheritance-problems/gene_mapping/two-point_test_cross-which_genotypes.py](problems/inheritance-problems/gene_mapping/two-point_test_cross-which_genotypes.py).

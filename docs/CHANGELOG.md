# Changelog

## 2025-12-27
- Added [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md) to document repo organization.
- Added [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md) to describe major components
  and generation flow.
- Added [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md) to outline generator
  refactoring and helper adoption steps.
- Added a higher-level pedigree scenario helper in
  [inheritance-problems/pedigrees/pedigree_template_gen_lib.py](inheritance-problems/pedigrees/pedigree_template_gen_lib.py)
  to select inheritance-specific templates and return pedigree code strings.
- Added pedigree PNG rendering alongside HTML output in
  [inheritance-problems/pedigrees/pedigree_png_lib.py](inheritance-problems/pedigrees/pedigree_png_lib.py).
- Added pedigree SVG rendering alongside HTML/PNG output in
  [inheritance-problems/pedigrees/pedigree_svg_lib.py](inheritance-problems/pedigrees/pedigree_svg_lib.py).
- Added pedigree code validators in
  [inheritance-problems/pedigrees/pedigree_validate_lib.py](inheritance-problems/pedigrees/pedigree_validate_lib.py).
- Split pedigree tooling into focused libraries:
  [inheritance-problems/pedigrees/pedigree_code_lib.py](inheritance-problems/pedigrees/pedigree_code_lib.py),
  [inheritance-problems/pedigrees/pedigree_html_lib.py](inheritance-problems/pedigrees/pedigree_html_lib.py),
  [inheritance-problems/pedigrees/pedigree_png_lib.py](inheritance-problems/pedigrees/pedigree_png_lib.py).
- Removed the unused compatibility shim `inheritance-problems/pedigrees/pedigree_lib.py`.
- Added inheritance mode validation in
  [inheritance-problems/pedigrees/pedigree_mode_validate_lib.py](inheritance-problems/pedigrees/pedigree_mode_validate_lib.py).
- Added a preview helper for HTML/PNG pedigree output in
  [inheritance-problems/pedigrees/preview_pedigree.py](inheritance-problems/pedigrees/preview_pedigree.py).
- Renamed pedigree template helpers for clarity:
  [inheritance-problems/pedigrees/pedigree_template_gen_lib.py](inheritance-problems/pedigrees/pedigree_template_gen_lib.py)
  and [inheritance-problems/pedigrees/pedigree_code_templates.py](inheritance-problems/pedigrees/pedigree_code_templates.py).
- Added strict CodeString validation (syntax checks plus bounding-box limits) and
  preview gating in
  [inheritance-problems/pedigrees/pedigree_validate_lib.py](inheritance-problems/pedigrees/pedigree_validate_lib.py)
  and [inheritance-problems/pedigrees/preview_pedigree.py](inheritance-problems/pedigrees/preview_pedigree.py).
- Simplified [inheritance-problems/pedigrees/preview_pedigree.py](inheritance-problems/pedigrees/preview_pedigree.py)
  CLI by baking in the strict validation defaults for width/height and attempts.
- Renamed pedigree question generators for clarity:
  [inheritance-problems/pedigrees/write_pedigree_choice.py](inheritance-problems/pedigrees/write_pedigree_choice.py) and
  [inheritance-problems/pedigrees/write_pedigree_match.py](inheritance-problems/pedigrees/write_pedigree_match.py).
- Added a graph-based pedigree generator in
  [inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](inheritance-problems/pedigrees/pedigree_graph_parse_lib.py).
- Split graph generation concerns into
  [inheritance-problems/pedigrees/pedigree_skeleton_lib.py](inheritance-problems/pedigrees/pedigree_skeleton_lib.py)
  and [inheritance-problems/pedigrees/pedigree_inheritance_lib.py](inheritance-problems/pedigrees/pedigree_inheritance_lib.py),
  leaving `pedigree_graph_parse_lib.py` as the IR and layout helper.
- Improved pedigree layout ordering to group siblings by parent index and reduce
  long connector spans in
  [inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](inheritance-problems/pedigrees/pedigree_graph_parse_lib.py).
- Added a basic three-generation layout smoke test helper in
  [inheritance-problems/pedigrees/pedigree_skeleton_lib.py](inheritance-problems/pedigrees/pedigree_skeleton_lib.py)
  and a small runner in
  [inheritance-problems/pedigrees/layout_smoke_test.py](inheritance-problems/pedigrees/layout_smoke_test.py).
- Added a simple CodeString renderer in
  [inheritance-problems/pedigrees/code_render.py](inheritance-problems/pedigrees/code_render.py)
  for HTML/PNG output from a provided code string.
- Extended [inheritance-problems/pedigrees/code_render.py](inheritance-problems/pedigrees/code_render.py)
  to support SVG output.
- Added semantic validation in
  [inheritance-problems/pedigrees/code_render.py](inheritance-problems/pedigrees/code_render.py)
  so invalid CodeStrings fail fast before rendering.
- Added a validation rule that vertical descent cannot terminate on a couple
  midpoint (`T`) in
  [inheritance-problems/pedigrees/pedigree_validate_lib.py](inheritance-problems/pedigrees/pedigree_validate_lib.py).
- Added progress logging and rejection summaries to
  [inheritance-problems/pedigrees/preview_pedigree.py](inheritance-problems/pedigrees/preview_pedigree.py).
- Documented pedigree CodeString symbols in
  [inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Documented CodeString semantics (row parity, couple/offspring encoding, and
  padding rules) in
  [inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Added row-parity semantics validation in
  [inheritance-problems/pedigrees/pedigree_validate_lib.py](inheritance-problems/pedigrees/pedigree_validate_lib.py).
- Tightened pedigree layout packing (component grouping and compact spacing) in
  [inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](inheritance-problems/pedigrees/pedigree_graph_parse_lib.py),
  and refined row-parity semantics to allow spouse connectors on people rows.
- Centered the top-generation couple in rendered layouts by applying a column
  shift during CodeString rendering in
  [inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](inheritance-problems/pedigrees/pedigree_graph_parse_lib.py).
- Implemented subtree-centered slot assignment for graph layouts in
  [inheritance-problems/pedigrees/pedigree_graph_parse_lib.py](inheritance-problems/pedigrees/pedigree_graph_parse_lib.py)
  to keep siblings contiguous and reduce long connector runs.
- Added a compact pedigree graph spec parser/serializer in
  [inheritance-problems/pedigrees/pedigree_graph_spec_lib.py](inheritance-problems/pedigrees/pedigree_graph_spec_lib.py)
  and documented the pedigree graph spec format in
  [inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Clarified in [inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md)
  that graph parsing/compilation is an internal, non-persisted step.
- Added a local pipeline note in
  [inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).
- Expanded [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md) with decision points
  for return contracts, shortfalls, newline policy, and argparse composition.
- Added question collection helpers and shared CLI args to [bptools.py](bptools.py).
- Updated [TEMPLATE.py](TEMPLATE.py) and
  [inheritance-problems/unique_cross_phenotypes.py](inheritance-problems/unique_cross_phenotypes.py)
  to use the new helpers.
- Clarified helper contracts in [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md)
  to standardize `write_question(N, args)` and `write_question_batch(N, args)`.
- Added output helpers in [bptools.py](bptools.py) and updated
  [TEMPLATE.py](TEMPLATE.py) and
  [inheritance-problems/unique_cross_phenotypes.py](inheritance-problems/unique_cross_phenotypes.py)
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
- Updated `inheritance-problems/unique_cross_genotypes.py`,
  `inheritance-problems/unique_cross_phenotypes.py`, and
  `inheritance-problems/unique_gametes.py` to use the new helper system.
- Removed single-letter question format flags from `add_question_format_args` and
  added long-form aliases like `--multiple-choice` and `--fill-in-blank`.
- Updated `bptools.print_histogram()` to use `tabulate` with `fancy_grid` output.
- Updated `bptools.print_histogram()` to render choices as columns with a final
  TOTAL column.
- Fixed indentation in `inheritance-problems/unique_gametes.py`.
- Updated `biochemistry-problems/ionic_bond_amino_acids.py`,
  `biochemistry-problems/macromolecules_categorize_by_name.py`, and
  `biochemistry-problems/alpha_helix_h-bonds.py` to use shared helpers and
  standardized argparse bundles.
- Standardized `add_base_args` defaults to `duplicate_runs=2` and no max question
  cap by default.
- Fixed `biochemistry-problems/ionic_bond_amino_acids.py` to honor `--num-choices`.
- Set a default `max_questions` cap for batch output in
  `biochemistry-problems/macromolecules_categorize_by_name.py`.
- Added `add_base_args_batch()` in [bptools.py](bptools.py) and switched
  `biochemistry-problems/macromolecules_categorize_by_name.py` to use it.
- Added `make_arg_parser()` in [bptools.py](bptools.py) and updated scripts to
  use it for consistent parser defaults.
- Switched `inheritance-problems/unique_cross_genotypes.py` and
  `inheritance-problems/unique_cross_phenotypes.py` to `make_arg_parser()`.
- Added `tabulate` to [pip_requirements.txt](pip_requirements.txt).
- Refactored [dna_profiling-problems/hla_genotype.py](dna_profiling-problems/hla_genotype.py)
  to use standard argparse helpers and `collect_and_write_questions`.
- Refactored [cell_biology-problems/cell_surf-to-vol_ratio.py](cell_biology-problems/cell_surf-to-vol_ratio.py)
  to use standard argparse helpers and `collect_and_write_questions`.
- Refactored [laboratory-problems/vol-vol_solution_numeric.py](laboratory-problems/vol-vol_solution_numeric.py)
  to use batch helpers and rely on `-d/--duplicate-runs` for per-liquid repeats.
- Added a legacy-modernization checklist section to
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored [biostatistics-problems/descriptive_stats_google_sheet.py](biostatistics-problems/descriptive_stats_google_sheet.py)
  to use shared argparse and helper-driven question collection.
- Refactored [molecular_biology-problems/consensus_sequence_MC.py](molecular_biology-problems/consensus_sequence_MC.py)
  to use shared helpers, standardized args, and Blackboard MC formatting.
- Refactored [inheritance-problems/dihybrid_cross_epistatic_gene_interactions.py](inheritance-problems/dihybrid_cross_epistatic_gene_interactions.py)
  to use shared helpers and standardized args.
- Fixed prime-mode complementary sequence answers to use reverse complements and
  consistent 5'->3' display in
  [molecular_biology-problems/complementary_sequences.py](molecular_biology-problems/complementary_sequences.py).
- Added `reverse_complement()` to
  [molecular_biology-problems/seqlib.py](molecular_biology-problems/seqlib.py).
- Added an answer check script at
  [tests/check_complementary_sequences_prime.py](tests/check_complementary_sequences_prime.py).
- Refactored [molecular_biology-problems/complementary_sequences.py](molecular_biology-problems/complementary_sequences.py)
  to use the shared argparse and helper workflow.
- Updated `complementary_sequences.py` to use `-d/--duplicate-runs` and
  `-x/--max-questions` instead of a custom `--num-sequences` argument.
- Added inline HTML style presets in
  [molecular_biology-problems/seqlib.py](molecular_biology-problems/seqlib.py)
  for consistent table borders and monospace cells.
- Added simple assertion tests for core helpers in
  [molecular_biology-problems/seqlib.py](molecular_biology-problems/seqlib.py).
- Added short descriptions for all `*lib.py` modules in
  [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md).
- Added [docs/TODO.md](docs/TODO.md) to track backlog items (including a possible
  `make_outfile_from_args()` helper).
- Refactored [biochemistry-problems/quick_fatty_acid_colon_system.py](biochemistry-problems/quick_fatty_acid_colon_system.py)
  to use batch helpers and `bptools` formatting.
- Refactored [inheritance-problems/cytogenetic_notation-aneuploidy.py](inheritance-problems/cytogenetic_notation-aneuploidy.py)
  to use shared argparse, question helpers, and unified output handling.
- Refactored [laboratory-problems/serial_dilution_factor_mc.py](laboratory-problems/serial_dilution_factor_mc.py)
  to use batch helpers and a computed default duplicate count.
- Added migration notes for batch upgrades in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored [molecular_biology-problems/rna_transcribe_fill_blank.py](molecular_biology-problems/rna_transcribe_fill_blank.py)
  to use shared argparse helpers and question collection.
- Kept [biostatistics-problems/make_html_box_plot.py](biostatistics-problems/make_html_box_plot.py)
  as a helper-only HTML utility (not a question generator).
- Refactored [laboratory-problems/serial_dilution_factor_diluent_numeric.py](laboratory-problems/serial_dilution_factor_diluent_numeric.py)
  to use batch helpers and a computed default duplicate count.
- Added a migration note for raw HTML emitters in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored [laboratory-problems/percent_dilution_aliquot_numeric.py](laboratory-problems/percent_dilution_aliquot_numeric.py)
  to use batch helpers and a fixed default duplicate count.
- Fixed an HTML paragraph nesting error in
  [laboratory-problems/percent_dilution_aliquot_numeric.py](laboratory-problems/percent_dilution_aliquot_numeric.py).
- Refactored [inheritance-problems/blood_type_offspring.py](inheritance-problems/blood_type_offspring.py)
  to use batch helpers with a shared parser and outfile builder.
- Refactored [inheritance-problems/probabiliy_of_progeny.py](inheritance-problems/probabiliy_of_progeny.py)
  to use shared argparse defaults and helper-based question collection.
- Refactored [inheritance-problems/chisquare/chi_square_errors.py](inheritance-problems/chisquare/chi_square_errors.py)
  to use shared argparse defaults and helper-based question collection.
- Added a migration note for fixed-grid batch scripts in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Converted laboratory generators from batch to per-question writers (Option 2
  selection) in:
  [laboratory-problems/mass_solution_numeric.py](laboratory-problems/mass_solution_numeric.py),
  [laboratory-problems/orders_of_magnitude_mc.py](laboratory-problems/orders_of_magnitude_mc.py),
  [laboratory-problems/percent_dilution_aliquot_numeric.py](laboratory-problems/percent_dilution_aliquot_numeric.py),
  [laboratory-problems/pipet_size_mc.py](laboratory-problems/pipet_size_mc.py),
  [laboratory-problems/serial_dilution_factor_diluent_numeric.py](laboratory-problems/serial_dilution_factor_diluent_numeric.py),
  [laboratory-problems/serial_dilution_factor_mc.py](laboratory-problems/serial_dilution_factor_mc.py),
  [laboratory-problems/vol-vol_solution_numeric.py](laboratory-problems/vol-vol_solution_numeric.py),
  [laboratory-problems/weight-vol_solution_numeric.py](laboratory-problems/weight-vol_solution_numeric.py).
- Added monospace formatting for numeric volumes/units across laboratory question
  text and choices (including dilution factor, percent dilution, mass/volume,
  molar solution, pipet, and serial dilution scripts).
- Removed unused [logger_config.py](logger_config.py).
- Fixed HTML quoting in [molecular_biology-problems/seqlib.py](molecular_biology-problems/seqlib.py)
  to avoid invalid inline style attributes.
- Added max-questions early-stop handling in
  [molecular_biology-problems/overhang_type.py](molecular_biology-problems/overhang_type.py).
- Fixed malformed HTML attributes in
  [molecular_biology-problems/enhancer_gene_expression.py](molecular_biology-problems/enhancer_gene_expression.py).
- Fixed paragraph nesting in
  [inheritance-problems/chisquare/chi_square_hardy_weinberg.py](inheritance-problems/chisquare/chi_square_hardy_weinberg.py).
- Implemented missing choice generation in
  [inheritance-problems/cytogenetic_notation-sub-band_notation.py](inheritance-problems/cytogenetic_notation-sub-band_notation.py).
- Fixed HTML entity formatting in
  [biochemistry-problems/fatty_acid_naming.py](biochemistry-problems/fatty_acid_naming.py).
- Fixed HTML paragraph closure in
  [molecular_biology-problems/rna_transcribe_prime_fill_blank.py](molecular_biology-problems/rna_transcribe_prime_fill_blank.py).
- Quoted HTML attribute values in
  [molecular_biology-problems/exon_splicing.py](molecular_biology-problems/exon_splicing.py)
  to satisfy XML parsing.
- Corrected outfile suffix selection in
  [inheritance-problems/hardy_weinberg_numeric.py](inheritance-problems/hardy_weinberg_numeric.py).
- Added max-questions early-stop handling in
  [inheritance-problems/pedigrees/write_pedigree_match.py](inheritance-problems/pedigrees/write_pedigree_match.py).
- Improved dilution factor MC choices and formatting (clarified labels, background
  explanation, colored aliquot/diluent with monospace values, and standardized
  `--num-choices`) in
  [laboratory-problems/dilution_factor_mc.py](laboratory-problems/dilution_factor_mc.py).
- De-duplicated numeric pH choices to avoid repeated labels in
  [biochemistry-problems/buffers/optimal_buffering_range.py](biochemistry-problems/buffers/optimal_buffering_range.py).
- Cleaned unused imports and a redundant global in [bptools.py](bptools.py) to
  satisfy pyflakes.
- Fixed a pyflakes warning in
  [biochemistry-problems/buffers/bufferslib.py](biochemistry-problems/buffers/bufferslib.py)
  by validating pKa values without unused variables.
- Fixed a bad error message variable in
  [biochemistry-problems/carbohydrates_classification/sugarlib.py](biochemistry-problems/carbohydrates_classification/sugarlib.py).
- Removed an unused import and a bad escape sequence in
  [biochemistry-problems/aminoacidlib.py](biochemistry-problems/aminoacidlib.py).
- Removed unused imports/vars in
  [biochemistry-problems/proteinlib.py](biochemistry-problems/proteinlib.py) and
  [dna_profiling-problems/gellib.py](dna_profiling-problems/gellib.py).
- Refactored [laboratory-problems/dilution_factor_calc_numeric.py](laboratory-problems/dilution_factor_calc_numeric.py)
  to use shared argparse defaults and helper-based question collection.
- Refactored [biochemistry-problems/which_lipid-chemical_formula.py](biochemistry-problems/which_lipid-chemical_formula.py)
  to use `bptools` MC formatting and shared helpers instead of manual text output.
- Refactored [inheritance-problems/dihybrid_cross_epistatic_gene_metabolics.py](inheritance-problems/dihybrid_cross_epistatic_gene_metabolics.py)
  to use shared argparse defaults, helper-based question collection, and remove
  debug prints.
- Added a migration note about preserving cyclic scenario selection in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored [biochemistry-problems/buffers/pKa_buffer_state.py](biochemistry-problems/buffers/pKa_buffer_state.py)
  to use batch helpers and a shared parser while preserving proton-count logic.
- Refactored [inheritance-problems/poisson_flies.py](inheritance-problems/poisson_flies.py)
  to use shared argparse defaults and helper-based question collection.
- Refactored [biochemistry-problems/chymotrypsin_substrate.py](biochemistry-problems/chymotrypsin_substrate.py)
  to use shared helpers, and moved the `--max-length` short flag from `-x` to `-M`
  to avoid conflict with `-x/--max-questions`.
- Updated [biochemistry-problems/chymotrypsin_substrate.py](biochemistry-problems/chymotrypsin_substrate.py)
  to map RasMol families to the custom palette, keep RasMol for the “weird”
  residues, and darken gray residues for white backgrounds.
- Added a migration note about `-x` short-flag conflicts in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Simplified `bptools.add_choice_args()` to a fixed API with a single `default=`
  parameter, and updated scripts to use that form.
- Set `biochemistry-problems/alpha_helix_h-bonds.py` to use
  `add_choice_args(..., default=4)`.
- Added `bptools.get_repo_data_path()` and switched
  `biochemistry-problems/isoelectric_two_proteins.py` to use it for data file
  resolution.
- Switched `biochemistry-problems/isoelectric_one_protein.py`,
  `biochemistry-problems/carbohydrates_classification/sugarlib.py`,
  `biochemistry-problems/proteinlib.py`, and `inheritance-problems/disorderlib.py`
  to use `bptools.get_repo_data_path()` for data file resolution.
- Switched `biochemistry-problems/PUBCHEM/wordle_peptides.py` and
  `inheritance-problems/deletion_mutant_words.py` to use
  `bptools.get_repo_data_path()` for data file resolution, and removed the
  local `get_git_root()` helper from
  `biochemistry-problems/carbohydrates_classification/sugarlib.py`.
- Refactored [biochemistry-problems/isoelectric_two_proteins.py](biochemistry-problems/isoelectric_two_proteins.py)
  to use shared argparse defaults, cached protein data, and helper-based output.
- Refactored [inheritance-problems/epistasis_test_cross.py](inheritance-problems/epistasis_test_cross.py)
  to use shared argparse defaults, helper-based question collection, and
  standardized outfile naming.
- Refactored [molecular_biology-problems/mutant_screen.py](molecular_biology-problems/mutant_screen.py)
  to use shared argparse defaults, MC/FIB format flags, and helper-based output.
- Fixed the mutant screen HTML table to quote the width attribute for valid XML
  in [molecular_biology-problems/mutant_screen.py](molecular_biology-problems/mutant_screen.py).
- Refactored [molecular_biology-problems/pcr_design.py](molecular_biology-problems/pcr_design.py)
  to use shared argparse defaults and helper-based MC formatting.
- Refactored [inheritance-problems/polyploid-monoploid_v_haploid.py](inheritance-problems/polyploid-monoploid_v_haploid.py)
  to use batch helpers and shared argparse defaults.
- Refactored [laboratory-problems/serial_dilution_factor_aliquot_numeric.py](laboratory-problems/serial_dilution_factor_aliquot_numeric.py)
  to use batch helpers and a computed default duplicate count.
- Added a migration note about preserving computed duplicate defaults for batch
  scripts in [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Switched [inheritance-problems/polyploid-monoploid_v_haploid.py](inheritance-problems/polyploid-monoploid_v_haploid.py)
  and [laboratory-problems/serial_dilution_factor_aliquot_numeric.py](laboratory-problems/serial_dilution_factor_aliquot_numeric.py)
  to non-batch question generation with scenario selection modes.
- Set the default duplicates for
  [laboratory-problems/serial_dilution_factor_aliquot_numeric.py](laboratory-problems/serial_dilution_factor_aliquot_numeric.py)
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
- Refactored [molecular_biology-problems/overhang_sequence.py](molecular_biology-problems/overhang_sequence.py)
  to use batch helpers, shared argparse defaults, and unified outfile naming.
- Refactored [inheritance-problems/pedigrees/write_pedigree_match.py](inheritance-problems/pedigrees/write_pedigree_match.py)
  to use batch helpers and start-numbered matching sets.
- Refactored [biochemistry-problems/Henderson-Hasselbalch.py](biochemistry-problems/Henderson-Hasselbalch.py)
  to use shared argparse defaults and helper-based question collection.
- Added a migration note about start-numbering for batch-generated lists in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Set defaults for question format/direction in
  [molecular_biology-problems/complementary_sequences.py](molecular_biology-problems/complementary_sequences.py)
  and [inheritance-problems/epistasis_test_cross.py](inheritance-problems/epistasis_test_cross.py)
  so they run without required flags.
- Set default question formats in
  [molecular_biology-problems/overhang_sequence.py](molecular_biology-problems/overhang_sequence.py)
  and [biochemistry-problems/Henderson-Hasselbalch.py](biochemistry-problems/Henderson-Hasselbalch.py)
  so they run without required flags.
- Set defaults for `alpha_helix_h-bonds.py` question type and
  `pKa_buffer_state.py` proton count, and fixed the overhang script to use the
  `question_type` dest so it runs without required flags.
- Fixed `add_question_format_args()` to always use `question_type` and updated
  callers (`complementary_sequences`, `overhang_sequence`, `alpha_helix_h-bonds`,
  `mutant_screen`, and `TEMPLATE.py`) to stop overriding dest.
- Fixed an indentation error in
  [biochemistry-problems/alpha_helix_h-bonds.py](biochemistry-problems/alpha_helix_h-bonds.py).
- Fixed duplicate argparse base-arg registration in
  [inheritance-problems/unique_gametes.py](inheritance-problems/unique_gametes.py).
- Added a max-questions early-exit check to
  [molecular_biology-problems/overhang_sequence.py](molecular_biology-problems/overhang_sequence.py)
  to avoid long full-list runs when `-x` is set.
- Refactored [laboratory-problems/molar_solution_using_mw_numeric.py](laboratory-problems/molar_solution_using_mw_numeric.py)
  to use shared argparse defaults and helper-based question collection.
- Refactored [molecular_biology-problems/translate_genetic_code.py](molecular_biology-problems/translate_genetic_code.py)
  to use shared argparse defaults, cached data reads, and helper-based question collection.
- Refactored [biochemistry-problems/fret_overlap_colors.py](biochemistry-problems/fret_overlap_colors.py)
  to use shared argparse defaults, MC formatting helpers, and randomized question selection.
- Added migration notes about replacing custom `-q/--num-questions` flags and
  about using repo data helpers in [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Refactored biochemistry scripts to use shared argparse defaults and helper-based
  question collection:
  [biochemistry-problems/buffers/optimal_buffering_range.py](biochemistry-problems/buffers/optimal_buffering_range.py),
  [biochemistry-problems/fatty_acid_naming.py](biochemistry-problems/fatty_acid_naming.py),
  [biochemistry-problems/fret_permute_colors.py](biochemistry-problems/fret_permute_colors.py),
  [biochemistry-problems/isoelectric_one_protein.py](biochemistry-problems/isoelectric_one_protein.py),
  [biochemistry-problems/metabolic_pathway_allosteric.py](biochemistry-problems/metabolic_pathway_allosteric.py),
  [biochemistry-problems/metabolic_pathway_inhibitor.py](biochemistry-problems/metabolic_pathway_inhibitor.py),
  [biochemistry-problems/michaelis_menten_table-inhibition.py](biochemistry-problems/michaelis_menten_table-inhibition.py),
  [biochemistry-problems/michaelis_menten_table-Km.py](biochemistry-problems/michaelis_menten_table-Km.py),
  [biochemistry-problems/optimal_enzyme-type_1.py](biochemistry-problems/optimal_enzyme-type_1.py),
  [biochemistry-problems/optimal_enzyme-type_2.py](biochemistry-problems/optimal_enzyme-type_2.py),
  [biochemistry-problems/optimal_enzyme-type_3.py](biochemistry-problems/optimal_enzyme-type_3.py),
  [biochemistry-problems/photosynthetic_light_pigments.py](biochemistry-problems/photosynthetic_light_pigments.py),
  [biochemistry-problems/protein_gel_migration.py](biochemistry-problems/protein_gel_migration.py),
  [biochemistry-problems/which_hydrophobic-simple.py](biochemistry-problems/which_hydrophobic-simple.py).
- Refactored biostatistics scripts to use shared argparse defaults and helper-based
  question collection:
  [biostatistics-problems/babies_two_sample_t_test.py](biostatistics-problems/babies_two_sample_t_test.py),
  [biostatistics-problems/busse_woods_one_sample_tests.py](biostatistics-problems/busse_woods_one_sample_tests.py),
  [biostatistics-problems/busse_woods_two_sample_t_test.py](biostatistics-problems/busse_woods_two_sample_t_test.py),
  [biostatistics-problems/population_test_google_sheet.py](biostatistics-problems/population_test_google_sheet.py),
  [biostatistics-problems/z_score_google_sheet.py](biostatistics-problems/z_score_google_sheet.py),
  [biostatistics-problems/z_score_table_interp.py](biostatistics-problems/z_score_table_interp.py).
- Refactored DNA profiling scripts to use shared argparse defaults, helper-based
  question collection, and parameter wrappers:
  [dna_profiling-problems/blood_type_agglutination_test.py](dna_profiling-problems/blood_type_agglutination_test.py),
  [dna_profiling-problems/who_father_html.py](dna_profiling-problems/who_father_html.py),
  [dna_profiling-problems/who_killer_html.py](dna_profiling-problems/who_killer_html.py).
- Refactored inheritance scripts to use shared argparse defaults and helper-based
  question collection or batch helpers:
  [inheritance-problems/blood_type_mother.py](inheritance-problems/blood_type_mother.py),
  [inheritance-problems/chisquare/chi_square_calculated.py](inheritance-problems/chisquare/chi_square_calculated.py),
  [inheritance-problems/chisquare/chi_square_choices.py](inheritance-problems/chisquare/chi_square_choices.py),
  [inheritance-problems/chisquare/chi_square_hardy_weinberg.py](inheritance-problems/chisquare/chi_square_hardy_weinberg.py),
  [inheritance-problems/cytogenetic_notation-rearrangements.py](inheritance-problems/cytogenetic_notation-rearrangements.py),
  [inheritance-problems/cytogenetic_notation-sub-band_notation.py](inheritance-problems/cytogenetic_notation-sub-band_notation.py),
  [inheritance-problems/deletion_mutant_random.py](inheritance-problems/deletion_mutant_random.py),
  [inheritance-problems/deletion_mutant_words.py](inheritance-problems/deletion_mutant_words.py),
  [inheritance-problems/dominant_and_X-linked_recessive.py](inheritance-problems/dominant_and_X-linked_recessive.py),
  [inheritance-problems/hardy_weinberg_mc_type.py](inheritance-problems/hardy_weinberg_mc_type.py),
  [inheritance-problems/hardy_weinberg_numeric.py](inheritance-problems/hardy_weinberg_numeric.py),
  [inheritance-problems/horses.py](inheritance-problems/horses.py),
  [inheritance-problems/letter_translocation_problem_color.py](inheritance-problems/letter_translocation_problem_color.py),
  [inheritance-problems/monohybrid_degrees_of_dominance.py](inheritance-problems/monohybrid_degrees_of_dominance.py),
  [inheritance-problems/monohybrid_genotype_statements.py](inheritance-problems/monohybrid_genotype_statements.py),
  [inheritance-problems/old_deletion_mutants.py](inheritance-problems/old_deletion_mutants.py),
  [inheritance-problems/pedigrees/write_pedigree_choice.py](inheritance-problems/pedigrees/write_pedigree_choice.py),
  [inheritance-problems/polyploid-gametes.py](inheritance-problems/polyploid-gametes.py),
  [inheritance-problems/punnett_choice.py](inheritance-problems/punnett_choice.py),
  [inheritance-problems/robertsonian.py](inheritance-problems/robertsonian.py),
  [inheritance-problems/translocation_meiosis_table.py](inheritance-problems/translocation_meiosis_table.py).
- Refactored laboratory scripts to use shared argparse defaults and helper-based
  question collection:
  [laboratory-problems/dilution_factor_aliquot_numeric.py](laboratory-problems/dilution_factor_aliquot_numeric.py),
  [laboratory-problems/dilution_factor_diluent_numeric.py](laboratory-problems/dilution_factor_diluent_numeric.py),
  [laboratory-problems/dilution_factor_mc.py](laboratory-problems/dilution_factor_mc.py),
  [laboratory-problems/mass_solution_numeric.py](laboratory-problems/mass_solution_numeric.py),
  [laboratory-problems/orders_of_magnitude_mc.py](laboratory-problems/orders_of_magnitude_mc.py),
  [laboratory-problems/pipet_size_mc.py](laboratory-problems/pipet_size_mc.py),
  [laboratory-problems/weight-vol_solution_numeric.py](laboratory-problems/weight-vol_solution_numeric.py).
- Refactored molecular biology scripts to use shared argparse defaults and helper-based
  question collection:
  [molecular_biology-problems/amplicon_copies.py](molecular_biology-problems/amplicon_copies.py),
  [molecular_biology-problems/beadle_tatum-metabolic_pathway.py](molecular_biology-problems/beadle_tatum-metabolic_pathway.py),
  [molecular_biology-problems/chargaff_dna_percent.py](molecular_biology-problems/chargaff_dna_percent.py),
  [molecular_biology-problems/consensus_sequence_FIB-arbitrary_code.py](molecular_biology-problems/consensus_sequence_FIB-arbitrary_code.py),
  [molecular_biology-problems/consensus_sequence_FIB-easy.py](molecular_biology-problems/consensus_sequence_FIB-easy.py),
  [molecular_biology-problems/consensus_sequence_FIB-hard.py](molecular_biology-problems/consensus_sequence_FIB-hard.py),
  [molecular_biology-problems/dna_gel-closest_farthest_MC.py](molecular_biology-problems/dna_gel-closest_farthest_MC.py),
  [molecular_biology-problems/dna_gel-estimate_size-MC_or_NUM.py](molecular_biology-problems/dna_gel-estimate_size-MC_or_NUM.py),
  [molecular_biology-problems/dna_melting_temp.py](molecular_biology-problems/dna_melting_temp.py),
  [molecular_biology-problems/enhancer_gene_expression.py](molecular_biology-problems/enhancer_gene_expression.py),
  [molecular_biology-problems/exon_splicing.py](molecular_biology-problems/exon_splicing.py),
  [molecular_biology-problems/inverse_pcr_design.py](molecular_biology-problems/inverse_pcr_design.py),
  [molecular_biology-problems/linear_digest.py](molecular_biology-problems/linear_digest.py),
  [molecular_biology-problems/nested_pcr_design.py](molecular_biology-problems/nested_pcr_design.py),
  [molecular_biology-problems/overhang_type.py](molecular_biology-problems/overhang_type.py),
  [molecular_biology-problems/palindrome_sequence_match.py](molecular_biology-problems/palindrome_sequence_match.py),
  [molecular_biology-problems/rna_transcribe_prime_fill_blank.py](molecular_biology-problems/rna_transcribe_prime_fill_blank.py),
  [molecular_biology-problems/rna_transcribe_prime.py](molecular_biology-problems/rna_transcribe_prime.py),
  [molecular_biology-problems/RT-qPCR.py](molecular_biology-problems/RT-qPCR.py).
- Implemented a working RT-qPCR numeric generator in
  [molecular_biology-problems/RT-qPCR.py](molecular_biology-problems/RT-qPCR.py),
  including randomized Ct tables and fold-change calculations.
- Added difficulty presets for parameter-heavy restriction digest generation in
  [molecular_biology-problems/linear_digest.py](molecular_biology-problems/linear_digest.py).
- Added difficulty presets for parameter-heavy generators:
  [molecular_biology-problems/nested_pcr_design.py](molecular_biology-problems/nested_pcr_design.py),
  [inheritance-problems/deletion_mutant_words.py](inheritance-problems/deletion_mutant_words.py),
  [inheritance-problems/deletion_mutant_random.py](inheritance-problems/deletion_mutant_random.py),
  [dna_profiling-problems/hla_genotype.py](dna_profiling-problems/hla_genotype.py),
  [biochemistry-problems/PUBCHEM/polypeptide_mc_sequence.py](biochemistry-problems/PUBCHEM/polypeptide_mc_sequence.py).
- Removed non-generator utilities from the phase-1 upgrade list and tracked them
  as utilities instead: 
  [inheritance-problems/pedigrees/pedigree_code_templates.py](inheritance-problems/pedigrees/pedigree_code_templates.py),
  [inheritance-problems/population_logistic_map_chaos.py](inheritance-problems/population_logistic_map_chaos.py).

# Changelog

## 2025-12-27
- Added [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md) to document repo organization.
- Added [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md) to describe major components
  and generation flow.
- Added [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md) to outline generator
  refactoring and helper adoption steps.
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
- Added a migration note about `-x` short-flag conflicts in
  [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md).
- Simplified `bptools.add_choice_args()` to a fixed API with a single `default=`
  parameter, and updated scripts to use that form.
- Set `biochemistry-problems/alpha_helix_h-bonds.py` to use
  `add_choice_args(..., default=4)`.

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

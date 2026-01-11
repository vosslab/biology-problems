# Code architecture

## Overview

The repository provides standalone Python scripts that generate biology quiz and homework questions for Genetics, Biochemistry, Molecular Biology, Cell Biology, and Biostatistics. Each generator script runs independently via CLI and emits question items in Blackboard upload format or human-readable HTML.

Generators randomize question content using inline logic, external data files, and shared helper functions. Output formats target Blackboard text upload (`bbq-*.txt`), QTI packages (`qti*.zip`), and HTML previews (`selftest-*.html`).

## Major components

### Generator scripts

- Located under `problems/*-problems/` subdirectories organized by domain.
- Most scripts are standalone executables with `#!/usr/bin/env python3` shebang.
- Use `argparse` for CLI flags with both short and long forms.
- Support `--help` to display usage and available options.
- Generate questions with randomization for anti-cheating and variation.
- Write output files following `bbq-<script_name>-...` naming convention.

### Shared helpers

- `bptools.py`: central formatting and utility module used by most generators.
  - Wraps `qti_package_maker` item types for multiple-choice, matching, and numeric questions.
  - Provides Blackboard text upload formatters (`formatBB_MC_Question`, `formatBB_MA_Question`, etc.).
  - Applies anti-cheat transforms (hidden terms, no-click divs).
  - Validates HTML output.
  - Generates answer histograms and summary statistics.
- `logger_config.py`: logging configuration used for consistent log output.

### Library modules

- Domain-specific helper libraries (e.g., `aminoacidlib.py`, `genotypelib.py`, `seqlib.py`).
- Located within their corresponding `problems/*-problems/` subdirectories.
- Provide specialized data structures, calculations, and formatting for specific question types.
- Examples: protein pI calculations, chi-square analysis, pedigree rendering, buffer systems.

### Content inputs

- `data/`: YAML, CSV, and text files with reference data (genetic disorders, protein tables, word lists).
- `matching_sets/`: YAML banks for matching question templates.
- `problems/multiple_choice_statements/`: YAML banks for statement-based multiple-choice items.
- Content files are loaded at runtime and often combined with randomization logic.

### Assets

- `images/`: static PNG, SVG, and JPG images referenced in question HTML.
- `javascript/`: small JS utilities embedded in HTML output for interactive previews.

### Templates

- `problems/TEMPLATE.py`: standard script layout with argparse setup and output conventions.
- Copy this template when creating new generators.

## Data flow

1. Script parses CLI arguments using `argparse` (duplicates, question format, output mode).
2. Generator assembles question content from inline logic, random variation, and data file lookups.
3. Question text and choices are built as HTML fragments using shared formatters from `bptools.py`.
4. Anti-cheat transforms are applied (hidden terms, choice shuffling, no-click protection).
5. HTML validation runs via `qti_package_maker.assessment_items.validator`.
6. Output is written to `bbq-*.txt` files in Blackboard upload format.
7. Answer histograms and question counts are printed to console for validation.

## Testing and verification

- No repo-wide unit test runner.
- Tests live in `tests/` and include:
  - `run_pyflakes.sh`: static analysis for syntax errors and unused imports.
  - `test_bptools.py`: pytest tests for core `bptools.py` functions.
  - `test_lib_imports.py`: checks library import integrity.
  - `tests/libs/`: pytest tests for specific library modules.
  - `tests/yaml/`: YAML data validation tests.
- Validate changes by running modified scripts and inspecting output formatting.
- Use `python3 data/check_yaml.py <file.yml>` to validate YAML inputs.

## Extension points

### Adding a new generator

1. Copy `problems/TEMPLATE.py` to the appropriate `problems/*-problems/` subdirectory.
2. Rename to match the question topic using snake_case.
3. Update argparse help text, question generation logic, and output filename.
4. Use `bptools.py` formatters for output consistency.
5. Run `pyflakes` and test with sample invocations.

### Adding new content

- Place YAML/CSV/text inputs under `data/` or matching_sets/.
- Add static images under `images/`.
- Use existing loaders (e.g., `yaml_tools` from `qti_package_maker`) or custom parsers.

### Extending shared helpers

- Add new helpers to `bptools.py` when logic is shared across multiple generators.
- Prefer single-purpose functions over large multipurpose utilities.
- Follow [docs/PYTHON_STYLE.md](PYTHON_STYLE.md) (tabs, type hints, docstrings).

## Known gaps

- Generator scripts use `qti_package_maker` as an external dependency; API changes require shim patches (see `bptools.py`).
- Some legacy scripts do not yet use the `bptools.py` framework (see `tools/bptools_scripts_audit.md`).
- Pedigree rendering requires external `rsvg-convert` for SVG-to-PNG conversion.

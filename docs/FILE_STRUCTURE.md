# File structure

## Top-level layout

- `problems/`: domain-specific question generators organized in subdirectories.
- `bptools.py`: shared formatting and utility helpers used by most generators.
- `logger_config.py`: logging configuration module.
- `data/`: YAML, CSV, and text inputs for question content (genetic disorders, protein tables, word lists).
- `images/`: static images (PNG, SVG, JPG) referenced in question HTML.
- `javascript/`: small JS utilities embedded in HTML outputs.
- `matching_sets/`: YAML banks for matching question templates.
- `tools/`: small utilities (markdown TOC generation, import analysis, auditing scripts).
- `tests/`: lightweight test scripts and pytest tests for validation.
- `docs/`: repository documentation and style guides.
- `devel/`: development utilities for changelog commits and PyPI publishing.
- `refactor-Jan_2026/`: refactoring workspace and upgrade tracking.
- `pip_requirements.txt`: Python dependencies for generators and tooling.
- `pyproject.toml`: project metadata, version, and build configuration.
- `source_me.sh`: environment setup script for Python 3.12.
- `AGENTS.md`: agent instructions and repository workflow guardrails.
- `README.md`: project overview, examples, and table of contents.
- `LICENSE`: GPL-3.0-or-later license text.
- `.gitignore`: ignored outputs (`bbq-*.txt`, `qti*.zip`, `selftest-*.html`, etc.).
- `VERSION`: current release version synced with `pyproject.toml`.

## Problem generator subdirectories

- `problems/biochemistry-problems/`: biochemistry generators (isoelectric point, gel migration, enzymes, sugars, etc.).
- `problems/biostatistics-problems/`: statistics and analysis generators (chi-squared, probability, distributions).
- `problems/cell_biology-problems/`: cell biology generators.
- `problems/dna_profiling-problems/`: DNA profiling and gel electrophoresis generators.
- `problems/inheritance-problems/`: genetics and inheritance generators (blood types, gametes, epistasis, pedigrees, gene mapping).
- `problems/laboratory-problems/`: lab-focused question generators.
- `problems/molecular_biology-problems/`: molecular biology generators (sequences, restriction enzymes, transcription/translation).
- `problems/matching_sets/`: content subdirectory for matching question YAML banks (not a problem domain).
- `problems/multiple_choice_statements/`: content subdirectory for statement-based MC YAML banks (not a problem domain).
- `problems/TEMPLATE.py`: template script for creating new generators.

## Library modules

Domain-specific helper libraries located within their corresponding `problems/*-problems/` subdirectories.

### Biochemistry libraries

- `aminoacidlib.py`: amino acid structure and HTML formula helpers.
- `buffers/bufferslib.py`: buffer system data (pKa, states, color sets).
- `carbohydrates_classification/sugarlib.py`: carbohydrate nomenclature and HTML table helpers.
- `enzymelib.py`: enzyme pH/temperature tables and randomized enzyme sets.
- `metaboliclib.py`: colored letter utilities for metabolic pathway labeling.
- `proteinlib.py`: protein pI/MW parsing and isoelectric point helpers.
- `PUBCHEM/aminoacidlib.py`: amino acid formula parsing with PubChem data.
- `PUBCHEM/moleculelib.py`: SMILES/CRC helpers and inline HTML molecule rendering.
- `PUBCHEM/pubchemlib.py`: PubChem REST client with YAML caching.

### Genetics libraries

- `chisquare/chisquarelib.py`: chi-square helpers (p-values, critical values).
- `deletionlib.py`: deletion mapping and ordering helpers.
- `disorderlib.py`: genetic disorder scenario generator using `data/genetic_disorders.yml`.
- `genemapping/genemaplib.py`: gene mapping, colored phenotype tables, recombination utilities.
- `genemapping/tetradlib.py`: tetrad analysis table helpers for meiosis mapping.
- `genotypelib.py`: genotype formatting, letter generation, combinatorics.
- `hybridcrosslib.py`: dihybrid/epistasis utilities and ratio dictionaries.

### Pedigree libraries

- `pedigrees/pedigree_lib/template_generator.py`: pedigree scenario picker for mode-specific templates.
- `pedigrees/pedigree_lib/code_templates.py`: curated pedigree code templates by inheritance mode.
- `pedigrees/pedigree_lib/validation.py`: pedigree code validation helpers.
- `pedigrees/pedigree_lib/code_definitions.py`: pedigree code constants and helpers.
- `pedigrees/pedigree_lib/html_output.py`: HTML rendering for pedigree code strings.
- `pedigrees/pedigree_lib/svg_output.py`: SVG rendering and SVG-to-PNG conversion.
- `pedigrees/pedigree_lib/graph_parse.py`: graph-based pedigree types and layout.
- `pedigrees/pedigree_lib/skeleton.py`: procedural pedigree skeleton generation.
- `pedigrees/pedigree_lib/inheritance_assign.py`: inheritance-mode phenotype assignment.
- `pedigrees/pedigree_lib/graph_spec.py`: compact pedigree IR string format parsers.
- `pedigrees/pedigree_lib/mode_validate.py`: inheritance mode validation for pedigrees.
- `pedigrees/pedigree_lib/preview_pedigree.py`: CLI helper for generating HTML/PNG previews.
- `pedigrees/PEDIGREE_PIPELINE.md`: local architecture note on pedigree rendering pipeline.

### Molecular biology and DNA profiling libraries

- `dna_profiling-problems/gellib.py`: gel electrophoresis band generation using PIL.
- `molecular_biology-problems/restrictlib.py`: restriction enzyme lookup and analysis (Biopython, web queries).
- `molecular_biology-problems/seqlib.py`: DNA/RNA sequence utilities (complements, transcription/translation, HTML tables).

## Data and content banks

- `data/`: YAML, CSV, HTML, and text inputs used by generators.
  - `genetic_disorders.yml`: genetic disorder data.
  - `cytogenetic_disorders.yml`: cytogenetic disorder data.
  - `organism_data.yml`: organism reference data.
  - `protein_isoelectric_points.csv`: protein pI/MW table.
  - `sugar_codes.yml`: carbohydrate structure codes.
  - `all_short_words.txt`, `enable2k.txt`, `real_wordles.txt`, `SCOWL-words_with_friends-intersection.txt`, `words_with_friends_dictionary.txt`: word lists.
- `matching_sets/`: YAML banks and templates for matching questions.
- `problems/multiple_choice_statements/`: YAML banks and helper scripts for statement-based MC questions.
- `images/`: static images referenced by HTML question text.
- `javascript/`: small JS assets for HTML outputs and testing.

## Tools and tests

### Tools directory

- `audit_problem_scripts_bptools_framework.py`: audits scripts for `bptools.py` framework usage.
- `build_question_function_index.py`: generates question function index documentation.
- `build_yaml_question_bank_index.py`: generates YAML question bank index.
- `check_yaml.py`: YAML validation and pretty-print utility for repo YAML inputs.
- `commit_changelog.py`: automates changelog commit workflow.
- `find_all_imports.py`: scans Python imports for dependency audits.
- `gh-md-toc`: GitHub Markdown table of contents generator.
- `allow_partial_credit_for_pool.py`: Blackboard pool partial credit utility.
- `convertAll.sh`: batch conversion script.

### Tests directory

- `run_pyflakes.sh`: static analysis with pyflakes.
- `test_bptools.py`: pytest tests for `bptools.py`.
- `test_lib_imports.py`: library import integrity checks.
- `tests/libs/`: pytest tests for specific library modules.
- `tests/yaml/`: YAML data validation tests.
- `conftest.py`: pytest configuration and fixtures.
- `lib_test_utils.py`: shared test utilities.

## Generated artifacts

Generated outputs are ignored by git (see `.gitignore`).

- `bbq-*.txt`: Blackboard text upload format question files.
- `qti*.zip`: QTI package exports.
- `selftest-*.html`: HTML preview files for question self-testing.
- `pyflakes.txt`: pyflakes static analysis output.
- `*.py[cod]`: compiled Python bytecode.
- `.DS_Store`: macOS folder metadata.

## Documentation map

All documentation lives in `docs/` except for root-level files required by convention.

- `docs/CODE_ARCHITECTURE.md`: system design, components, and data flow.
- `docs/FILE_STRUCTURE.md`: directory map and file organization (this file).
- `docs/PYTHON_STYLE.md`: Python coding style and conventions.
- `docs/REPO_STYLE.md`: repository-level organization and file placement rules.
- `docs/MARKDOWN_STYLE.md`: Markdown writing and formatting conventions.
- `docs/CHANGELOG.md`: chronological user-facing record of changes.
- `docs/TODO.md`: backlog scratchpad for small tasks.
- `docs/QUESTION_AUTHORING_GUIDE.md`: guide for writing new question generators.
- `docs/QUESTION_FUNCTION_INDEX.md`: index of question generation functions.
- `docs/YAML_QUESTION_BANK_INDEX.md`: index of YAML question banks.
- `docs/AUTHORS.md`: primary maintainers and contributors.
- `docs/UNIFICATION_PLAN.md`: plan for unifying script interfaces.

Root-level docs (required by convention):

- `AGENTS.md`: agent instructions and repository workflow guardrails.
- `README.md`: project purpose, examples, and quick start.
- `LICENSE`: GPL-3.0-or-later license text.

## Where to add new work

### New question generators

- Copy `problems/TEMPLATE.py` to the appropriate `problems/*-problems/` subdirectory.
- Rename to match the question topic using snake_case.
- Update argparse help text, question logic, and output filename.

### New library modules

- Place domain-specific helpers in the corresponding `problems/*-problems/` subdirectory.
- Name with `*lib.py` suffix for consistency.
- Import and use from generator scripts in the same subdirectory.

### New content inputs

- Place YAML/CSV/text inputs under `data/`.
- Place matching question banks under `matching_sets/`.
- Place statement-based MC banks under `problems/multiple_choice_statements/`.
- Add static images under `images/`.

### New tests

- Add pytest tests under `tests/` or `tests/libs/` as appropriate.
- Add YAML validation tests under `tests/yaml/`.
- Run `tests/run_pyflakes.sh` for static analysis after changes.

### New documentation

- Place new docs under `docs/` using SCREAMING_SNAKE_CASE filenames.
- Update `docs/CHANGELOG.md` when making changes.
- Follow [docs/MARKDOWN_STYLE.md](MARKDOWN_STYLE.md) for formatting.

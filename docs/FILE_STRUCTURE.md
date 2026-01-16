# File structure

## Top-level layout

- [AGENTS.md](AGENTS.md): agent instructions and workflow guardrails.
- [README.md](README.md): repo overview, quick start, and doc links.
- [docs/](docs/): repository documentation and style guides.
- [problems/](problems/): generator scripts, domain libraries, and content banks.
- [data/](data/): YAML/CSV/text inputs used by generators.
- [images/](images/): static images referenced by question HTML.
- [tests/](tests/): pytest suites and lint helpers.
- [tools/](tools/): utilities for audits and index generation.
- [devel/](devel/): local development helpers.
- [refactor-Jan_2026/](refactor-Jan_2026/): refactor tracking workspace.
- [source_me.sh](source_me.sh): environment setup for Python 3.12.
- [pip_requirements.txt](pip_requirements.txt): Python dependencies.
- [pyproject.toml](pyproject.toml): project metadata and build config.
- [Brewfile](Brewfile): optional Homebrew dependencies.
- [LICENSE](LICENSE): GPL-3.0-or-later license text.
- [VERSION](VERSION): repo version string.
- [MANIFEST.in](MANIFEST.in): package include list.
- [matching_sets/](matching_sets/): empty placeholder directory.

## Problem generator subdirectories

- [problems/biochemistry-problems/](problems/biochemistry-problems/): biochemistry generators and libraries.
- [problems/biostatistics-problems/](problems/biostatistics-problems/): statistics and analysis generators.
- [problems/cell_biology-problems/](problems/cell_biology-problems/): cell biology generators.
- [problems/dna_profiling-problems/](problems/dna_profiling-problems/): DNA profiling and gel electrophoresis.
- [problems/inheritance-problems/](problems/inheritance-problems/): genetics and inheritance generators.
- [problems/laboratory-problems/](problems/laboratory-problems/): lab-focused generators.
- [problems/molecular_biology-problems/](problems/molecular_biology-problems/): molecular biology generators.
- [problems/matching_sets/](problems/matching_sets/): YAML banks for matching questions.
- [problems/multiple_choice_statements/](problems/multiple_choice_statements/): YAML banks and tools for statement-based MC questions.
- [problems/TEMPLATE.py](problems/TEMPLATE.py): generator script template.

## Library modules

Domain-specific helper libraries live near the generators that use them.

### Biochemistry libraries

- [problems/biochemistry-problems/aminoacidlib.py](problems/biochemistry-problems/aminoacidlib.py): amino acid helpers.
- [problems/biochemistry-problems/buffers/bufferslib.py](problems/biochemistry-problems/buffers/bufferslib.py): buffer system data.
- [problems/biochemistry-problems/carbohydrates_classification/sugarlib.py](problems/biochemistry-problems/carbohydrates_classification/sugarlib.py): carbohydrate nomenclature utilities.
- [problems/biochemistry-problems/PUBCHEM/pubchemlib.py](problems/biochemistry-problems/PUBCHEM/pubchemlib.py): PubChem REST client and caching.
- [problems/biochemistry-problems/PUBCHEM/moleculelib.py](problems/biochemistry-problems/PUBCHEM/moleculelib.py): molecule rendering and SMILES helpers.

### Genetics libraries

- [problems/inheritance-problems/chi_square/chisquarelib.py](problems/inheritance-problems/chi_square/chisquarelib.py): chi-square helpers.
- [problems/inheritance-problems/deletion_mutants/deletionlib.py](problems/inheritance-problems/deletion_mutants/deletionlib.py): deletion mapping helpers.
- [problems/inheritance-problems/gene_mapping/genemaplib.py](problems/inheritance-problems/gene_mapping/genemaplib.py): gene mapping utilities.
- [problems/inheritance-problems/gene_mapping/tetradlib.py](problems/inheritance-problems/gene_mapping/tetradlib.py): tetrad analysis utilities.
- [problems/inheritance-problems/genotypelib.py](problems/inheritance-problems/genotypelib.py): genotype formatting helpers.

### Pedigree libraries

- [problems/inheritance-problems/pedigrees/pedigree_lib/](problems/inheritance-problems/pedigrees/pedigree_lib/): pedigree graph parsing, rendering, and validation.
- [problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md): pedigree pipeline overview.

### Molecular biology and DNA profiling libraries

- [problems/dna_profiling-problems/gellib.py](problems/dna_profiling-problems/gellib.py): gel electrophoresis helpers.
- [problems/molecular_biology-problems/restrictlib.py](problems/molecular_biology-problems/restrictlib.py): restriction enzyme lookup and analysis.
- [problems/molecular_biology-problems/seqlib.py](problems/molecular_biology-problems/seqlib.py): sequence utilities.

### Phylogenetic tree libraries

- [problems/inheritance-problems/phylogenetic_trees/treelib/](problems/inheritance-problems/phylogenetic_trees/treelib/): tree generation, sorting, and rendering helpers.

## Data and content banks

- [data/](data/): YAML/CSV/text inputs used by generators.
- [problems/matching_sets/](problems/matching_sets/): matching-set YAML banks by topic.
- [problems/multiple_choice_statements/](problems/multiple_choice_statements/): statement-based MC YAML banks and utilities.
- [images/](images/): static PNG/JPG assets referenced in question HTML.

## Tools and tests

### Tools directory

- [tools/audit_problem_scripts_bptools_framework.py](tools/audit_problem_scripts_bptools_framework.py): framework usage audit.
- [tools/build_question_function_index.py](tools/build_question_function_index.py): question-function index generator.
- [tools/build_yaml_question_bank_index.py](tools/build_yaml_question_bank_index.py): YAML bank index generator.
- [tools/check_yaml.py](tools/check_yaml.py): YAML validation and pretty-print utility.
- [tools/commit_changelog.py](tools/commit_changelog.py): changelog helper.
- [tools/find_all_imports.py](tools/find_all_imports.py): import scan utility.
- [tools/allow_partial_credit_for_pool.py](tools/allow_partial_credit_for_pool.py): Blackboard pool helper.
- [tools/convertAll.sh](tools/convertAll.sh): batch conversion script.
- [tools/get_function_counts.sh](tools/get_function_counts.sh): function count summary.
- [tools/gh-md-toc](tools/gh-md-toc): Markdown table-of-contents generator.
- [tools/remove_all_bbq_files.sh](tools/remove_all_bbq_files.sh): cleanup helper for generated BBQ files.

### Tests directory

- [tests/run_pyflakes.sh](tests/run_pyflakes.sh): pyflakes lint runner.
- [tests/run_ascii_compliance.py](tests/run_ascii_compliance.py): repo-wide ASCII/ISO compliance check.
- [tests/check_ascii_compliance.py](tests/check_ascii_compliance.py): single-file ASCII/ISO compliance check.
- [tests/test_bptools.py](tests/test_bptools.py): core `bptools` tests.
- [tests/test_lib_imports.py](tests/test_lib_imports.py): import integrity checks.
- [tests/libs/](tests/libs/): library-specific pytest coverage.
- [tests/yaml/](tests/yaml/): YAML validation tests.

## Generated artifacts

Generated outputs are ignored by git (see [.gitignore](.gitignore)).

- `bbq-*.txt`: Blackboard text upload format question files.
- `qti*.zip`: QTI package exports.
- `selftest-*.html`: HTML preview files for question self-testing.
- `pyflakes.txt`: pyflakes static analysis output.
- `ascii_compliance.txt`: ASCII compliance output from tests.
- `*.py[cod]`: compiled Python bytecode.
- `.DS_Store`: macOS folder metadata.
- `*.html`: includes generated HTML like [all_gene_trees-3-leaves.html](all_gene_trees-3-leaves.html).

## Documentation map

All documentation lives in [docs/](docs/) except for root-level files required by convention.

- [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md): system design, components, and data flow.
- [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md): directory map and file organization.
- [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md): Python coding style and conventions.
- [docs/REPO_STYLE.md](docs/REPO_STYLE.md): repository-level organization and file placement rules.
- [docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md): Markdown writing and formatting conventions.
- [docs/CHANGELOG.md](docs/CHANGELOG.md): chronological user-facing record of changes.
- [docs/TODO.md](docs/TODO.md): backlog scratchpad for small tasks.
- [docs/QUESTION_AUTHORING_GUIDE.md](docs/QUESTION_AUTHORING_GUIDE.md): guide for writing new question generators.
- [docs/QUESTION_FUNCTION_INDEX.md](docs/QUESTION_FUNCTION_INDEX.md): index of question generation functions.
- [docs/YAML_QUESTION_BANK_INDEX.md](docs/YAML_QUESTION_BANK_INDEX.md): index of YAML question banks.
- [docs/AUTHORS.md](docs/AUTHORS.md): primary maintainers and contributors.
- [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md): plan for unifying script interfaces.

Root-level docs (required by convention):

- [AGENTS.md](AGENTS.md): agent instructions and repository workflow guardrails.
- [README.md](README.md): project purpose, examples, and quick start.
- [LICENSE](LICENSE): GPL-3.0-or-later license text.

## Where to add new work

### New question generators

- Copy [problems/TEMPLATE.py](problems/TEMPLATE.py) to the appropriate `problems/*-problems/` subdirectory.
- Rename to match the question topic using snake_case.
- Update argparse help text, question logic, and output filename.

### New library modules

- Place domain-specific helpers in the corresponding `problems/*-problems/` subdirectory.
- Use a `*lib.py` suffix for helper libraries when it improves clarity.
- Import and use from generator scripts in the same subdirectory.

### New content inputs

- Place shared YAML/CSV/text inputs under [data/](data/).
- Place matching question banks under [problems/matching_sets/](problems/matching_sets/).
- Place statement-based MC banks under [problems/multiple_choice_statements/](problems/multiple_choice_statements/).
- Add static images under [images/](images/).

### New tests

- Add pytest tests under [tests/](tests/) or [tests/libs/](tests/libs/) as appropriate.
- Add YAML validation tests under [tests/yaml/](tests/yaml/).
- Run [tests/run_pyflakes.sh](tests/run_pyflakes.sh) for static analysis after changes.

### New documentation

- Place new docs under [docs/](docs/) using SCREAMING_SNAKE_CASE filenames.
- Update [docs/CHANGELOG.md](docs/CHANGELOG.md) when making changes.
- Follow [docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md) for formatting.

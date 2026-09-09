# File structure

## Top-level layout

- [AGENTS.md](../AGENTS.md): agent instructions and workflow guardrails.
- [README.md](../README.md): repo overview, quick start, and doc links.
- docs/: repository documentation and style guides.
- `problems`: generator scripts, domain libraries, and content banks.
- `data`: YAML/CSV/text inputs used by generators.
- `images`: static images referenced by question HTML.
- `tests`: pytest suites and lint helpers.
- `tools`: utilities for audits, index generation, YAML, and images.
- `devel`: release and changelog tooling.
- [source_me.sh](../source_me.sh): environment setup for Python 3.12.
- [pip_requirements.txt](../pip_requirements.txt): Python dependencies.
- [Brewfile](../Brewfile): optional Homebrew dependencies.
- `LICENSE.LGPL_v3`: LGPLv3 license text for code.
- `LICENSE.CC_BY_4_0`: CC BY 4.0 license text for non-code content.
- [VERSION](../VERSION): repo version string.

## Problem generator subdirectories

- `biochemistry-problems`: biochemistry generators and libraries.
- `biophysics-problems`: biophysics generators (e.g. FRET color problems).
- `biostatistics-problems`: statistics and analysis generators.
- `cell_biology-problems`: cell biology generators.
- `dna_profiling-problems`: DNA profiling and gel electrophoresis.
- `inheritance-problems`: genetics and inheritance generators.
- `laboratory-problems`: lab-focused generators.
- `molecular_biology-problems`: molecular biology generators.
- `matching_sets`: YAML banks for matching questions.
- `multiple_choice_statements`: YAML banks and tools for statement-based MC questions.
- [TEMPLATE.py](../problems/TEMPLATE.py): generator script template.

## Library modules

Domain-specific helper libraries live near the generators that use them.

### Biochemistry libraries

- [aminoacidlib.py](../problems/biochemistry-problems/aminoacidlib.py): amino acid helpers.
- [bufferslib.py](../problems/biochemistry-problems/buffers/bufferslib.py): buffer system data.
- [sugarlib.py](../problems/biochemistry-problems/carbs/sugarlib.py): carbohydrate nomenclature utilities.
- [pubchemlib.py](../problems/biochemistry-problems/PUBCHEM/pubchemlib.py): PubChem REST client and caching.
- [moleculelib.py](../problems/biochemistry-problems/PUBCHEM/moleculelib.py): molecule rendering and SMILES helpers.

### Genetics libraries

- [chisquarelib.py](../problems/inheritance-problems/chi_square/chisquarelib.py): chi-square helpers.
- [deletionlib.py](../problems/inheritance-problems/deletion_mutants/deletionlib.py): deletion mapping helpers.
- [genemaplib.py](../problems/inheritance-problems/gene_mapping/genemaplib.py): gene mapping utilities.
- [tetradlib.py](../problems/inheritance-problems/gene_mapping/tetradlib.py): tetrad analysis utilities.
- [genotypelib.py](../problems/inheritance-problems/genotypelib.py): genotype formatting helpers.

### Pedigree libraries

- `pedigree_lib`: pedigree graph parsing, rendering, and validation.
- [PEDIGREE_PIPELINE.md](../problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md): pedigree pipeline overview.

### Molecular biology and DNA profiling libraries

- [gellib.py](../problems/dna_profiling-problems/gellib.py): gel electrophoresis helpers.
- [restrictlib.py](../problems/molecular_biology-problems/restriction_enzymes/restrictlib.py): restriction enzyme lookup and analysis.
- [seqlib.py](../problems/molecular_biology-problems/seqlib.py): sequence utilities.

### Phylogenetic tree libraries

- `treelib`: tree generation, sorting, and rendering helpers.

## Data and content banks

- `data`: YAML/CSV/text inputs used by generators.
- `matching_sets`: matching-set YAML banks by topic.
- `multiple_choice_statements`: statement-based MC YAML banks and utilities.
- `images`: static PNG/JPG assets referenced in question HTML.

## Tools and tests

### Tools directory

- [audit_problem_scripts_bptools_framework.py](../tools/audit_problem_scripts_bptools_framework.py): framework usage audit.
- [build_question_function_index.py](../tools/build_question_function_index.py): question-function index generator.
- [build_yaml_question_bank_index.py](../tools/build_yaml_question_bank_index.py): YAML bank index generator.
- [check_yaml.py](../tools/check_yaml.py): YAML validation and pretty-print utility.
- [add_dbsubject_to_yaml.py](../tools/add_dbsubject_to_yaml.py): add subject tags to YAML banks.
- [find_all_imports.py](../tools/find_all_imports.py): import scan utility.
- [allow_partial_credit_for_pool.py](../tools/allow_partial_credit_for_pool.py): Blackboard pool helper.
- [contrast_calculator.py](../tools/contrast_calculator.py): color contrast helper.
- [normalize_svg.py](../tools/normalize_svg.py): SVG normalization utility.
- [sync_membrane_svgs.py](../tools/sync_membrane_svgs.py): membrane SVG sync helper.
- [convertAll.sh](../tools/convertAll.sh): batch conversion script.
- [get_function_counts.sh](../tools/get_function_counts.sh): function count summary.
- [gh-md-toc](../tools/gh-md-toc): Markdown table-of-contents generator.
- [remove_all_bbq_files.sh](../tools/remove_all_bbq_files.sh): cleanup helper for generated BBQ files.

### Devel directory

Release and changelog tooling (sharing [changelog_lib.py](../devel/changelog_lib.py)).

- [bump_version.py](../devel/bump_version.py): version bump helper.
- [rotate_changelog.py](../devel/rotate_changelog.py): changelog rotation per repo policy.
- [query_changelog.py](../devel/query_changelog.py): changelog search by date/category/keyword.
- [commit_changelog.py](../devel/commit_changelog.py): seed commit message from changelog entries.
- [flatten_broken_md_links.py](../devel/flatten_broken_md_links.py): Markdown link repair helper.
- [dist_clean.sh](../devel/dist_clean.sh): build artifact cleanup.
- [setup_playwright.sh](../devel/setup_playwright.sh): Playwright setup.

### Tests directory

- [test_pyflakes_code_lint.py](../tests/test_pyflakes_code_lint.py): repo-wide pyflakes lint gate.
- [test_ascii_compliance.py](../tests/test_ascii_compliance.py): repo-wide ASCII/ISO compliance gate.
- [test_markdown_links.py](../tests/test_markdown_links.py): local Markdown link validation gate.
- [check_ascii_compliance.py](../tests/check_ascii_compliance.py): single-file ASCII/ISO compliance check.
- [fix_ascii_compliance.py](../tests/fix_ascii_compliance.py): single-file ASCII/ISO fixer.
- [test_bptools.py](../tests/test_bptools.py): core `bptools` tests.
- [test_lib_imports.py](../tests/test_lib_imports.py): import integrity checks.
- `libs`: library-specific pytest coverage.
- `yaml`: YAML validation tests.

## Generated artifacts

Generated outputs are ignored by git (see [.gitignore](../.gitignore)).

- `bbq-*.txt`: Blackboard text upload format question files.
- `blackboard_export_zip-*.zip`: validated Blackboard pool packages created with `--bbexport`.
- `qti*.zip`: QTI package exports.
- `selftest-*.html`: HTML preview files for question self-testing.
- `pyflakes.txt`: pyflakes static analysis output.
- `ascii_compliance.txt`: ASCII compliance output from tests.
- `*.py[cod]`: compiled Python bytecode.
- `.DS_Store`: macOS folder metadata.
- `*.html`: includes generated HTML such as `all_gene_trees-3-leaves.html`.

## Documentation map

All documentation lives in docs/ except for root-level files required by convention.

- [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md): system design, components, and data flow.
- [FILE_STRUCTURE.md](FILE_STRUCTURE.md): directory map and file organization.
- [PYTHON_STYLE.md](PYTHON_STYLE.md): Python coding style and conventions.
- [REPO_STYLE.md](REPO_STYLE.md): repository-level organization and file placement rules.
- [MARKDOWN_STYLE.md](MARKDOWN_STYLE.md): Markdown writing and formatting conventions.
- [CHANGELOG.md](CHANGELOG.md): chronological user-facing record of changes.
- [TODO.md](TODO.md): backlog scratchpad for small tasks.
- [QUESTION_AUTHORING_GUIDE.md](QUESTION_AUTHORING_GUIDE.md): guide for writing new question generators.
- [QUESTION_FUNCTION_INDEX.md](QUESTION_FUNCTION_INDEX.md): index of question generation functions.
- [YAML_QUESTION_BANK_INDEX.md](YAML_QUESTION_BANK_INDEX.md): index of YAML question banks.
- [AUTHORS.md](AUTHORS.md): primary maintainers and contributors.
- [UNIFICATION_PLAN.md](UNIFICATION_PLAN.md): plan for unifying script interfaces.

Root-level docs (required by convention):

- [AGENTS.md](../AGENTS.md): agent instructions and repository workflow guardrails.
- [README.md](../README.md): project purpose, examples, and quick start.
- `LICENSE.LGPL_v3`: LGPLv3 license text for code.
- `LICENSE.CC_BY_4_0`: CC BY 4.0 license text for non-code content.

## Where to add new work

### New question generators

- Copy [TEMPLATE.py](../problems/TEMPLATE.py) to the appropriate `problems/*-problems/` subdirectory.
- Rename to match the question topic using snake_case.
- Update argparse help text, question logic, and output filename.

### New library modules

- Place domain-specific helpers in the corresponding `problems/*-problems/` subdirectory.
- Use a `*lib.py` suffix for helper libraries when it improves clarity.
- Import and use from generator scripts in the same subdirectory.

### New content inputs

- Place shared YAML/CSV/text inputs under `data`.
- Place matching question banks under `matching_sets`.
- Place statement-based MC banks under `multiple_choice_statements`.
- Add static images under `images`.

### New tests

- Add pytest tests under `tests` or `libs` as appropriate.
- Add YAML validation tests under `yaml`.
- Run `pytest tests/` (includes the pyflakes, ASCII, and Markdown-link gates) after changes.

### New documentation

- Place new docs under docs/ using SCREAMING_SNAKE_CASE filenames.
- Update [CHANGELOG.md](CHANGELOG.md) when making changes.
- Follow [MARKDOWN_STYLE.md](MARKDOWN_STYLE.md) for formatting.

# Code architecture

## Overview

The repository provides standalone Python scripts under [problems/](../problems/) that generate biology quiz and homework items. Generators combine local logic with shared helpers in [bptools.py](../bptools.py) and reference inputs from [data/](../data/) plus content banks under [problems/matching_sets/](../problems/matching_sets/) and [problems/multiple_choice_statements/](../problems/multiple_choice_statements/).

Outputs commonly include Blackboard text files (`bbq-*.txt`), QTI packages (`qti*.zip`), and HTML previews (`selftest-*.html`) as listed in [.gitignore](../.gitignore).

## Major components

### Generator scripts

- Located under [problems/](../problems/) in `*-problems/` subfolders, organized by domain.
- Typically executable Python scripts with `argparse` CLIs and `--help`.
- Many use shared output helpers from [bptools.py](../bptools.py).

### Shared helpers

- [bptools.py](../bptools.py): formatting, output wrappers, HTML validation, and shared utilities built on `qti_package_maker`.

### Domain libraries

- Libraries live alongside generators in their domain folders, for example:
  - [problems/inheritance-problems/pedigrees/pedigree_lib/](../problems/inheritance-problems/pedigrees/pedigree_lib/): pedigree parsing, rendering, and validation.
  - [problems/inheritance-problems/phylogenetic_trees/treelib/](../problems/inheritance-problems/phylogenetic_trees/treelib/): phylogenetic tree generation helpers.
  - [problems/biochemistry-problems/PUBCHEM/](../problems/biochemistry-problems/PUBCHEM/): PubChem-backed molecule helpers and data.

### Content inputs and banks

- [data/](../data/): YAML/CSV/text reference data used by generators.
- [problems/matching_sets/](../problems/matching_sets/): YAML banks for matching questions.
- [problems/multiple_choice_statements/](../problems/multiple_choice_statements/): YAML banks and helpers for statement-based multiple choice.

### Assets

- [images/](../images/): static images referenced by question text/HTML.
- [problems/biochemistry-problems/PUBCHEM/PEPTIDES/PEPTIDYLE_WEB/](../problems/biochemistry-problems/PUBCHEM/PEPTIDES/PEPTIDYLE_WEB/): JS/CSS assets for peptide word games.

### Tooling and tests

- [tools/](../tools/): indexing, audit, YAML, and image utilities.
- [devel/](../devel/): release and changelog tooling, including versioning and changelog
  rotation/query helpers.
- [tests/](../tests/): pytest coverage and lint gates.

## Data flow

1. A generator script under [problems/](../problems/) parses CLI args with `argparse`.
2. The script loads reference data from [data/](../data/) or YAML banks under [problems/](../problems/).
3. Domain libraries and [bptools.py](../bptools.py) build question text, choices, and answer keys.
4. When used, `bptools` runs HTML validation via `qti_package_maker` and formats output.
5. Results are written to BBQ text files, QTI zips, or HTML previews in the repo root.

## Testing and verification

- Run the pytest suite with `pytest tests/`; coverage lives under [tests/](../tests/) and [tests/libs/](../tests/libs/).
- Repo-wide lint gates: [tests/test_pyflakes_code_lint.py](../tests/test_pyflakes_code_lint.py), [tests/test_ascii_compliance.py](../tests/test_ascii_compliance.py), and [tests/test_markdown_links.py](../tests/test_markdown_links.py). Single-file helpers: [tests/check_ascii_compliance.py](../tests/check_ascii_compliance.py) and [tests/fix_ascii_compliance.py](../tests/fix_ascii_compliance.py).
- Validate generator changes by running the modified scripts and inspecting output formatting.
- Validate YAML inputs with [tools/check_yaml.py](../tools/check_yaml.py) (supports directories with `--recursive`).

## Extension points

- New generators: copy [problems/TEMPLATE.py](../problems/TEMPLATE.py) into the appropriate domain folder.
- New data: place reference inputs in [data/](../data/) or content banks under [problems/matching_sets/](../problems/matching_sets/) and [problems/multiple_choice_statements/](../problems/multiple_choice_statements/).
- Shared logic: add reusable helpers to [bptools.py](../bptools.py) or domain libraries near the generators that use them.

## Known gaps

- None outstanding.

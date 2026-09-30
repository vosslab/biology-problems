# Code architecture

## Overview

The repository provides standalone Python scripts under `problems` that generate biology quiz and homework items. Generators combine local logic with shared helpers in [bptools.py](../bptools.py) and reference inputs from `data` plus content banks under `matching_sets` and `multiple_choice_statements`.

Outputs commonly include Blackboard text files (`bbq-*.txt`), validated Blackboard pool ZIPs
(`bez-*.zip`), QTI packages (`qti*.zip`), and HTML previews
(`selftest-*.html`) as listed in [.gitignore](../.gitignore).

## Major components

### Generator scripts

- Located under `problems` in `*-problems/` subfolders, organized by domain.
- Typically executable Python scripts with `argparse` CLIs and `--help`.
- Many use shared output helpers from [bptools.py](../bptools.py).

### Shared helpers

- [bptools.py](../bptools.py): formatting, output wrappers, HTML validation, and shared utilities built on `qti_package_maker`.

### Domain libraries

- Libraries live alongside generators in their domain folders, for example:
  - `pedigree_lib`: pedigree parsing, rendering, and validation.
  - `treelib`: phylogenetic tree generation helpers.
  - `PUBCHEM`: PubChem-backed molecule helpers and data.

### Content inputs and banks

- `data`: YAML/CSV/text reference data used by generators.
- `matching_sets`: YAML banks for matching questions.
- `multiple_choice_statements`: YAML banks and helpers for statement-based multiple choice.

### Assets

- `images`: static images referenced by question text/HTML.
- `PEPTIDYLE_WEB`: JS/CSS assets for peptide word games.

### Tooling and tests

- `tools`: indexing, audit, YAML, and image utilities.
- `devel`: release and changelog tooling, including versioning and changelog
  rotation/query helpers.
- `tests`: pytest coverage and lint gates.

## Data flow

1. A generator script under `problems` parses CLI args with `argparse`.
2. The script loads reference data from `data` or YAML banks under `problems`.
3. Domain libraries and [bptools.py](../bptools.py) build question text, choices, and answer keys.
4. When used, `bptools` runs HTML validation via `qti_package_maker` and formats output.
5. The shared writer stores BBQ text and, with `-B` / `--bbexport`, reads that retained file through
   `qti_package_maker` to create an adjacent validated Blackboard pool ZIP. Other conversion flows
   can write QTI ZIPs or HTML previews in the repo root.

## Testing and verification

- Run the pytest suite with `pytest tests/`; coverage lives under `tests` and `libs`.
- Repo-wide lint gates: [test_pyflakes_code_lint.py](../tests/test_pyflakes_code_lint.py), [test_ascii_compliance.py](../tests/test_ascii_compliance.py), and [test_markdown_links.py](../tests/test_markdown_links.py). Single-file helpers: [check_ascii_compliance.py](../tests/check_ascii_compliance.py) and [fix_ascii_compliance.py](../tests/fix_ascii_compliance.py).
- Validate generator changes by running the modified scripts and inspecting output formatting.
- Validate YAML inputs with `check_yaml.py` (supports directories with `--recursive`).

## Extension points

- New generators: copy [TEMPLATE.py](../problems/TEMPLATE.py) into the appropriate domain folder.
- New data: place reference inputs in `data` or content banks under `matching_sets` and `multiple_choice_statements`.
- Shared logic: add reusable helpers to [bptools.py](../bptools.py) or domain libraries near the generators that use them.

## Known gaps

- None outstanding.

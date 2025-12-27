# File structure

## Overview
- This repo is a collection of standalone Python generators for biology problem sets.
- Domain-specific generators live in `*-problems/` folders.
- Shared helpers live at the repo root.
- Input data and content banks live in `data/`, `matching_sets/`, and
  `multiple_choice_statements/`.
- Generated outputs are ignored by git; see `.gitignore` for `bbq-*.txt`, `qti*.zip`, and
  `selftest-*.html`.
- Follow [docs/REPO_STYLE.md](docs/REPO_STYLE.md) for naming and placement rules.

## Top-level directories
- `biochemistry-problems/`: biochemistry question generators.
- `biostatistics-problems/`: statistics and analysis generators.
- `cell_biology-problems/`: cell biology generators.
- `dna_profiling-problems/`: DNA profiling generators.
- `inheritance-problems/`: genetics and inheritance generators.
- `laboratory-problems/`: lab-focused question generators.
- `molecular_biology-problems/`: molecular biology generators.

## Shared code and templates
- `bptools.py`: shared formatting and utility helpers used by many generators.
- `logger_config.py`: optional logging setup for scripts that need it.
- `TEMPLATE.py`: starting point for new generators (argparse + output pattern).
- `find_all_imports.py`: helper for scanning Python imports when updating deps.

## Data and content banks
- `data/`: YAML/CSV/HTML/text inputs and reference tables used by generators.
- `matching_sets/`: YAML banks and templates for matching questions.
- `multiple_choice_statements/`: YAML banks and helper scripts for statement-based
  multiple choice.
- `images/`: static images referenced by HTML question text.
- `javascript/`: small JS assets for HTML outputs and testing.

## Tools and tests
- `tools/`: small utilities (for example, markdown TOC generation and conversion scripts).
- `tests/`: lightweight checks such as `run_pyflakes.sh`.

## Root-level docs and misc
- [README.md](README.md): broad description and sample output.
- [AGENTS.md](AGENTS.md): agent instructions and repository workflow guardrails.
- [LICENSE](LICENSE): repository licensing terms.
- `.gitignore`: ignored outputs and local artifacts.
- `docs/`: repo documentation (see [docs/REPO_STYLE.md](docs/REPO_STYLE.md)).
- `requirements.txt`: Python dependencies for generators and tooling.
- Word lists and scratch files: `SHORT_WORDS.txt`, `science.txt`, `science-count.txt`,
  `temp.txt`.

# Repository Guidelines

## Project Structure & Module Organization

- `problems/*-problems/`: domain-specific generators (Genetics, Biochemistry, Molecular Biology, etc.). Most files are standalone Python scripts that emit quiz/homework items.
- `bptools.py`, `logger_config.py`: shared helpers used by many generators (formatting, utilities).
- `data/`: YAML/CSV/text inputs used by generators (word lists, reference tables, datasets).
- `images/`: static images referenced in question text/HTML.
- `matching_sets/`, `problems/multiple_choice_statements/`: content banks used to assemble questions.
- `tools/`: small utilities (e.g., image conversion scripts).
- `read_qti/`: utilities for reading/converting QTI exports.

## Build, Test, and Development Commands

- Setup python3.12 environment
source REPO_ROOT/source_me.sh
- Run a generator (most support `--help` via `argparse`):
  - `python3 problems/inheritance-problems/<script>.py --help`
  - `python3 problems/biochemistry-problems/<script>.py -m -d 50` (example: generate 50 MC questions)
- Inspect YAML inputs:
  - `python3 data/check_yaml.py data/genetic_disorders.yml`

Generated artifacts (do not commit): `bbq-*.txt`, `qti*.zip`, `selftest-*.html` (see `.gitignore`).

## Coding Style & Naming Conventions

- Python: follow `docs/PYTHON_STYLE.md` (tabs for indentation; prefer Python ~3.12).
- Prefer executable scripts with `#!/usr/bin/env python3`, a `main()` entrypoint, and `if __name__ == '__main__': main()`.
- Use `argparse` with both short and long flags (e.g., `-d/--duplicates`), and keep output filenames predictable (often `bbq-<script>-...`).
- Keep comments ASCII-only; prefer f-strings; avoid `import *`.

## Testing Guidelines

- There is no repo-wide unit test runner. Validate changes by:
  - Running the modified script(s) and sanity-checking the generated output formatting.
  - Adding small `assert` checks for pure helper functions where appropriate.
- For student assessments, prefer true randomness in scenario selection (or a well-mixed PRNG-based selection) over deterministic round-robin/modulo cycling, since predictable sequences make cheating easier; use deterministic selection primarily for debugging, reproducibility, or unit tests.

## Commit & Pull Request Guidelines

- Git history uses short, imperative, free-form subjects (no Conventional Commits); keep subjects brief and specific (e.g., “fix wording”, “formatting tweaks”).
- PRs should describe the problem set affected (`problems/inheritance-problems/`, `problems/biochemistry-problems/`, etc.), how to reproduce (`python3 ...`), and include a small sample of expected output (or a screenshot if HTML/image rendering changes).
See Markdown style in docs/MARKDOWN_STYLE.md.
When making edits, document them in docs/CHANGELOG.md.
See repo style in docs/REPO_STYLE.md.
Agents may run programs in the tests folder, including smoke tests and pyflakes/mypy runner scripts.

## Environment
Codex must run Python using `/opt/homebrew/opt/python@3.12/bin/python3.12` (use Python 3.12 only).
On this user's macOS (Homebrew Python 3.12), Python modules are installed to `/opt/homebrew/lib/python3.12/site-packages/`.
When in doubt, implement the changes the user asked for rather than waiting for a response; the user is not the best reader and will likely miss your request and then be confused why it was not implemented or fixed.
When changing code always run tests, documentation does not require tests.

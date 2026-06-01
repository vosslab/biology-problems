# Repository guidelines

Standalone Python generators under `problems/*-problems/` emit quiz and homework
items via shared helpers in [bptools.py](bptools.py). For layout and design see
[docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md) and
[docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md).

## Style and workflow
- Python: [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md).
- Pytest: [docs/PYTEST_STYLE.md](docs/PYTEST_STYLE.md).
- Markdown: [docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md).
- Repo organization, git, commit, and changelog rules: [docs/REPO_STYLE.md](docs/REPO_STYLE.md).
- Document every change in [docs/CHANGELOG.md](docs/CHANGELOG.md).

## Run and test
- Setup and run: see [docs/INSTALL.md](docs/INSTALL.md) and [docs/USAGE.md](docs/USAGE.md).
- Bootstrap before running scripts: `source source_me.sh` (requires the sibling
  `qti-package-maker` repo cloned alongside).
- Run the test suite with `pytest tests/`.

## Repo-specific rules
- For student assessments, prefer true randomness in scenario selection over
  deterministic round-robin/modulo cycling; predictable sequences make cheating easier.
  Use deterministic selection only for debugging, reproducibility, or unit tests.

## Standing directives
- Codex must run Python using `/opt/homebrew/opt/python@3.12/bin/python3.12` (Python 3.12
  only); modules install to `/opt/homebrew/lib/python3.12/site-packages/`. This is Codex
  runtime only, not a requirement for repo scripts.
- When in doubt, implement the changes the user asked for rather than waiting for a
  response; the user is not the best reader and will likely miss your request and then be
  confused why it was not implemented or fixed.
- When changing code always run tests; documentation does not require tests.

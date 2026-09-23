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
- Run the test suite with `source source_me.sh && pytest tests/`.

## Repo-specific rules
- For student assessments, prefer true randomness in scenario selection over
  deterministic round-robin/modulo cycling; predictable sequences make cheating easier.
  Use deterministic selection only for debugging, reproducibility, or unit tests.

## Standing directives
- Agents must run Python using `source source_me.sh && python3`

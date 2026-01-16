# Biology problem generators

Python scripts that generate biochemistry, genetics, molecular biology, and related homework/quiz items for instructors and course staff. Inputs live in [data/](data/) and [images/](images/), and generators emit outputs such as `bbq-*.txt`, `qti*.zip`, and `selftest-*.html` (ignored by git).

## Documentation

### Getting started
- [docs/INSTALL.md](docs/INSTALL.md): Setup requirements and environment notes.
- [docs/USAGE.md](docs/USAGE.md): Common generator commands and flags.

### Getting oriented
- [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md): System overview and data flow.
- [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md): Directory map and where generators, data, and outputs belong.
- [docs/CHANGELOG.md](docs/CHANGELOG.md): Chronological record of repo changes.

### Authoring and indexes
- [docs/QUESTION_AUTHORING_GUIDE.md](docs/QUESTION_AUTHORING_GUIDE.md): How to write and review questions.
- [docs/QUESTION_FUNCTION_INDEX.md](docs/QUESTION_FUNCTION_INDEX.md): Index of generator scripts and functions.
- [docs/YAML_QUESTION_BANK_INDEX.md](docs/YAML_QUESTION_BANK_INDEX.md): Index of YAML-backed question banks.

### Standards
- [docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md): Markdown formatting rules for this repo.
- [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md): Python conventions for generator scripts and helpers.
- [docs/REPO_STYLE.md](docs/REPO_STYLE.md): Repo organization, naming, and workflow rules.

### Project notes
- [docs/AUTHORS.md](docs/AUTHORS.md): Maintainers and contributors.
- [docs/TODO.md](docs/TODO.md): Short backlog of small tasks.
- [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md): Plan for generator standardization work.

## Quick start
- `source source_me.sh`
- `/opt/homebrew/opt/python@3.12/bin/python3.12 problems/biochemistry-problems/Henderson-Hasselbalch.py -m -d 5`
- Review the generated `bbq-*.txt` output in the repo root.

## Status
- The detailed per-problem catalog is intentionally omitted here because it was out of date; use the indexes in [docs/QUESTION_FUNCTION_INDEX.md](docs/QUESTION_FUNCTION_INDEX.md) and [docs/YAML_QUESTION_BANK_INDEX.md](docs/YAML_QUESTION_BANK_INDEX.md) for current coverage.

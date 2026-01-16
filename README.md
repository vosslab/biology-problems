# Biology problem generators

Python scripts that generate biochemistry, genetics, molecular biology, and related homework/quiz items for instructors and course staff. Inputs live in `data/` and `images/`, and generators emit outputs such as `bbq-*.txt`, `qti*.zip`, and `selftest-*.html` (ignored by git).

## Documentation
- [docs/AUTHORS.md](docs/AUTHORS.md)
- [docs/CHANGELOG.md](docs/CHANGELOG.md)
- [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md)
- [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md)
- [docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md)
- [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md)
- [docs/QUESTION_AUTHORING_GUIDE.md](docs/QUESTION_AUTHORING_GUIDE.md)
- [docs/QUESTION_FUNCTION_INDEX.md](docs/QUESTION_FUNCTION_INDEX.md)
- [docs/REPO_STYLE.md](docs/REPO_STYLE.md)
- [docs/TODO.md](docs/TODO.md)
- [docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md)
- [docs/YAML_QUESTION_BANK_INDEX.md](docs/YAML_QUESTION_BANK_INDEX.md)

## Quick start
- `source source_me.sh`
- `/opt/homebrew/opt/python@3.12/bin/python3.12 problems/biochemistry-problems/Henderson-Hasselbalch.py -m -d 5`
- Review the generated `bbq-*.txt` output in the repo root.

## Status
- The detailed per-problem catalog is intentionally omitted here because it was out of date; use the indexes in [docs/QUESTION_FUNCTION_INDEX.md](docs/QUESTION_FUNCTION_INDEX.md) and [docs/YAML_QUESTION_BANK_INDEX.md](docs/YAML_QUESTION_BANK_INDEX.md) for current coverage.

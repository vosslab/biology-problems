# Biology problem generators

Python scripts that generate biochemistry, genetics, molecular biology, and related homework/quiz items for instructors and course staff. Inputs live in `data/` and `images/`, and generators emit outputs such as `bbq-*.txt`, `qti*.zip`, and `selftest-*.html` (ignored by git).

## Documentation
- [Authors](docs/AUTHORS.md)
- [Changelog](docs/CHANGELOG.md)
- [Code architecture](docs/CODE_ARCHITECTURE.md)
- [File structure](docs/FILE_STRUCTURE.md)
- [Markdown style](docs/MARKDOWN_STYLE.md)
- [Python style](docs/PYTHON_STYLE.md)
- [Question authoring guide](docs/QUESTION_AUTHORING_GUIDE.md)
- [Question function index](docs/QUESTION_FUNCTION_INDEX.md)
- [Repo style](docs/REPO_STYLE.md)
- [Todo list](docs/TODO.md)
- [Unification plan](docs/UNIFICATION_PLAN.md)
- [YAML question bank index](docs/YAML_QUESTION_BANK_INDEX.md)

## Quick start
- `source source_me.sh`
- `/opt/homebrew/opt/python@3.12/bin/python3.12 problems/biochemistry-problems/Henderson-Hasselbalch.py -m -d 5`
- Review the generated `bbq-*.txt` output in the repo root.

## Status
- The detailed per-problem catalog is intentionally omitted here because it was out of date; use the indexes in [Question function index](docs/QUESTION_FUNCTION_INDEX.md) and [YAML question bank index](docs/YAML_QUESTION_BANK_INDEX.md) for current coverage.

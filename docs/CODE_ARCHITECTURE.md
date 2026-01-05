# Code architecture

## Purpose
- The repo provides standalone scripts that generate biology quiz and homework items.
- Output targets include Blackboard upload text and human-readable previews.

## Major components
- Generator scripts: located under `problems/*-problems/`, each script is usually a standalone CLI.
- Shared helpers: `bptools.py` centralizes formatting, validation, and output helpers.
- Content inputs: `data/`, `matching_sets/`, and `problems/multiple_choice_statements/` provide YAML,
  CSV, and text banks.
- Assets: `images/` and `javascript/` support HTML content inside questions.
- Templates: `TEMPLATE.py` provides the standard script layout and output naming.

## Runtime flow
- Scripts parse CLI arguments with `argparse` and decide how many questions to generate.
- Question content is assembled from inline logic and/or data files, often with random
  variation for versions.
- Question text and choices are formatted as HTML fragments for Blackboard-compatible
  output.
- `bptools.py` wraps `qti_package_maker` item types, applies anti-cheat transforms,
  validates HTML, and formats output for Blackboard text uploads.
- Scripts write `bbq-*.txt` outputs and print stats (for example answer histograms).

## Shared helper responsibilities
- `bptools.py` provides formatting helpers (`formatBB_MC_Question`, `formatBB_MA_Question`,
  etc.).
- `bptools.py` provides HTML validation and string utilities via `qti_package_maker`.
- `bptools.py` provides answer histograms and common output conventions.

## Extension points
- Add a new generator by copying `TEMPLATE.py` into the relevant `problems/*-problems/` folder.
- Add new YAML/CSV/text inputs under `data/`, `matching_sets/`, or
  `problems/multiple_choice_statements/`.
- Prefer shared helpers in `bptools.py` over duplicating formatting logic.

## Related docs
- [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md)
- [docs/REPO_STYLE.md](docs/REPO_STYLE.md)
- [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md)

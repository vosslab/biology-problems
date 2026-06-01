# Install

"Installed" here means the generator scripts run from a source checkout with the
shared `bptools` helpers and the sibling `qti_package_maker` package importable.
There is no separate package install; you source the environment helper and run
scripts in place.

## Requirements
- Python 3.12 recommended; other Python 3 versions may work but are not guaranteed.
- The sibling repo `qti-package-maker` cloned next to this repo (provides
  `qti_package_maker`, required by [bptools.py](../bptools.py)).
- Python dependencies listed in [pip_requirements.txt](../pip_requirements.txt)
  (developer extras in [pip_requirements-dev.txt](../pip_requirements-dev.txt)).
- Optional Homebrew packages listed in [Brewfile](../Brewfile).
- Optional sibling repo `local-llm-wrapper` for the `topic_classifier` pipeline.

## Install steps
1. Clone this repo and `qti-package-maker` into the same parent directory.
2. From the repo root, source the environment helper (sets `PYTHONPATH`):
   - `source source_me.sh`
3. Install Python dependencies:
   - `pip install -r pip_requirements.txt`
   - `pip install -r pip_requirements-dev.txt` (for running the test suite)

## Verify install
- Run a generator's help to confirm imports resolve:
  - `python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --help`

## Known gaps
- [ ] Confirm exact minimum sibling-repo versions for `qti-package-maker`.
- [ ] Confirm supported platforms beyond macOS with Homebrew.

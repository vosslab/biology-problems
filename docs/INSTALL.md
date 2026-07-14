# Install

This repository is not a Python package. Setup means running its generator scripts directly from a
source checkout with the shared `bptools` helpers and the separately installed `qti_package_maker`
package importable. Source the environment helper and run scripts in place.

## Requirements
- Python 3.12 recommended; other Python 3 versions may work but are not guaranteed.
- The `qti-package-maker` distribution from PyPI, which provides the
  `qti_package_maker` module required by [bptools.py](../bptools.py).
- Python dependencies listed in [pip_requirements.txt](../pip_requirements.txt)
  (developer extras in [pip_requirements-dev.txt](../pip_requirements-dev.txt)).
- Optional Homebrew packages listed in [Brewfile](../Brewfile).
- Optional sibling repo `local-llm-wrapper` for the `topic_classifier` pipeline.

## Install steps
1. Clone this repository and enter its root directory.
2. Install the repository dependencies:
   - `python3 -m pip install -r pip_requirements.txt`
3. Install `qti-package-maker` separately from PyPI:
   - `python3 -m pip install qti-package-maker`
4. Source the environment helper, which adds this checkout to `PYTHONPATH`:
   - `source source_me.sh`

`qti-package-maker` intentionally remains outside `pip_requirements.txt` so its release can be
installed or developed independently.

## Develop both projects

Clone [`qti-package-maker`](https://github.com/vosslab/qti-package-maker) beside this repository
when developing both projects. `source_me.sh` places the sibling checkout before installed packages
on `PYTHONPATH`:

- `git clone https://github.com/vosslab/qti-package-maker.git`

Install the developer requirements when running this repository's test suite:

- `python3 -m pip install -r pip_requirements-dev.txt`

## Verify install
- Run a generator's help to confirm imports resolve:
  - `python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --help`

## Known gaps
- [ ] Confirm supported platforms beyond macOS with Homebrew.

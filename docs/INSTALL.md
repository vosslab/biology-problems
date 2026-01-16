# INSTALL.md

## Requirements
- macOS with Homebrew Python 3.12 installed at `/opt/homebrew/opt/python@3.12/bin/python3.12`.
- Repo dependencies listed in `pip_requirements.txt`.
- Optional system packages listed in `Brewfile`.

## Setup
1. From the repo root, source the environment helper:
   - `source source_me.sh`
2. Install Python dependencies if needed (see `pip_requirements.txt`).
3. Verify Python 3.12 is available:
   - `/opt/homebrew/opt/python@3.12/bin/python3.12 --version`

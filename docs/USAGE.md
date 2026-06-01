# Usage

Each script under [problems/](../problems/) is a standalone generator that emits
quiz or homework items. Most use shared helpers from [bptools.py](../bptools.py)
and a common `argparse` CLI. Run a script directly after sourcing the environment.

## Quick start
- `source source_me.sh`
- `python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --mc -d 5`
- Review the generated `bbq-*.txt` output in the repo root.

## CLI
Generators built on `bptools` share a common argument set (see any script's
`--help` for the authoritative list):

- `-d`, `--duplicates`: number of duplicate runs (questions to generate).
- `-x`, `--max-questions`: cap the total number of questions written.
- `-c`: number of answer choices.
- `--mc`, `--ma`, `--format {mc,ma,num}`: select the question format.
- `-h`, `--help`: show the full flag list for that script.

## Examples
- Generate 5 multiple-choice questions:
  - `python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --mc -d 5`
- Show a generator's full options:
  - `python3 problems/inheritance-problems/<script>.py --help`
- Validate a YAML input file:
  - `python3 tools/check_yaml.py data/genetic_disorders.yml`

## Inputs and outputs
- Inputs: YAML/CSV/text reference data in [data/](../data/), YAML banks under
  [problems/matching_sets/](../problems/matching_sets/) and
  [problems/multiple_choice_statements/](../problems/multiple_choice_statements/),
  and images in [images/](../images/).
- Outputs (written to the repo root, ignored by git): Blackboard `bbq-*.txt`
  files, QTI `qti*.zip` packages, and `selftest-*.html` previews.

## Known gaps
- [ ] Confirm which generators expose a `--dry-run` flag, if any.

# Usage

Each script under [problems/](../problems/) is a standalone generator that emits
quiz or homework items. Most use shared helpers from [bptools.py](../bptools.py)
and a common `argparse` CLI. Follow [INSTALL.md](INSTALL.md) to install
`qti-package-maker`, then run a script after sourcing the environment.

## Quick start

- `source source_me.sh`
- `python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --mc -d 5`
- Review the generated `bbq-*.txt` output in the repo root.

Add `--bbexport` when Blackboard needs an importable pool ZIP:

```bash
python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --mc -d 5 --bbexport
```

## CLI

Generators built on `bptools` share a common argument set (see any script's
`--help` for the authoritative list):

- `-d`, `--duplicates`: number of duplicate runs (questions to generate).
- `-x`, `--max-questions`: cap the total number of questions written.
- `-c`: number of answer choices.
- `--mc`, `--ma`, `--format {mc,ma,num}`: select the question format.
- `-B`, `--bbexport`: also create a Blackboard pool export ZIP.
- `--hidden-terms`: enable hidden decoy terms for Blackboard Learn Original.
- `--noclick-div`: enable the no-click wrapper for Blackboard Learn Original.
- `-h`, `--help`: show the full flag list for that script.

### Blackboard Ultra defaults

Hidden terms and the no-click wrapper are off by default. Hidden terms use visually hidden spans;
Ultra strips their CSS and can expose the decoy words. The no-click wrapper uses inline event
handlers that Ultra strips. The two Original-specific features remain available as explicit
opt-ins.

The Original-specific positive flags remain supported and may be deprecated if that compatibility
path is retired. The command surface omits redundant negative flags because all three features
default off.

This default covers the shared anti-cheat markup only. Authored color, scripts, and table layouts
can have separate Ultra limitations; see the
[ultra_classic_showcase_question_catalog.md](active_plans/reports/ultra_classic_showcase_question_catalog.md).

### Blackboard ZIP export

With `--bbexport`, each generator first retains its normal `bbq-<name>-questions.txt` file, then
creates `blackboard_export_zip-<name>.zip` beside it through the `qti_package_maker` library.
Supported export types are `MC`, `MA`, `MATCH`, `FIB`, `MULTI_FIB`, and `NUM`. Other types, including
`ORDER`, raise a clear error because the Blackboard export engine has no writer for them.

The ZIP replaces its destination only after it opens successfully and contains the Blackboard
manifest and pool data. A failed conversion retains the BBQ text for diagnosis and removes the new
temporary ZIP.

## Examples

- Generate 5 multiple-choice questions:
  - `python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --mc -d 5`
- Generate the same BBQ text plus a Blackboard pool export ZIP:
  - `python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --mc -d 5 -B`
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
  files, Blackboard `blackboard_export_zip-*.zip` packages, QTI `qti*.zip` packages, and
  `selftest-*.html` previews.

## Known gaps

- [ ] Confirm which generators expose a `--dry-run` flag, if any.

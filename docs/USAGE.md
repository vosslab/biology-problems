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

Add `-I` when the Blackboard ZIP must convert every HTML table into packaged PNGs:

```bash
python3 problems/dna_profiling-problems/blood_type_agglutination_test.py -d 5 -B -I
```

## CLI

Generators built on `bptools` share a common argument set (see any script's
`--help` for the authoritative list):

- `-d`, `--duplicates`: number of duplicate runs (questions to generate).
- `-x`, `--max-questions`: cap the total number of questions written.
- `-c`: number of answer choices.
- `--mc`, `--ma`, `--format {mc,ma,num}`: select the question format.
- `-B`, `--bbexport`: also create a Blackboard pool export ZIP.
- `-I`, `--html-to-image`: convert every HTML table and RDKit canvas to packaged PNGs in a `-B` ZIP.
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
creates `bez-<name>.zip` beside it through the `qti_package_maker` library.
Supported export types are `MC`, `MA`, `MATCH`, `FIB`, `MULTI_FIB`, and `NUM`. Other types, including
`ORDER`, raise a clear error because the Blackboard export engine has no writer for them.

The ZIP replaces its destination only after it opens successfully and contains the Blackboard
manifest and pool data. A failed conversion retains the BBQ text for diagnosis and removes the new
temporary ZIP.

`-I` is opt-in and requires `-B`. It uses `qti-package-maker` to screenshot every HTML table
and RDKit canvases, then embeds the resulting PNGs in the Blackboard ZIP. It requires the Python
`playwright` package and its Chromium browser; after installing package dependencies, run
`playwright install chromium`. Nested tables are included in the outer table's image. Missing RDKit only affects banks
that contain RDKit canvases.

## Examples

- Generate 5 multiple-choice questions:
  - `python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --mc -d 5`
- Generate the same BBQ text plus a Blackboard pool export ZIP:
  - `python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --mc -d 5 -B`
- Generate a Blackboard pool ZIP with packaged PNG drawings:
  - `python3 problems/dna_profiling-problems/blood_type_agglutination_test.py -d 5 -B -I`
- Show a generator's full options:
  - `python3 problems/inheritance-problems/<script>.py --help`
- Validate a YAML input file:
  - `python3 tools/check_yaml.py data/genetic_disorders.yml`

### RNA transcription

[rna_transcribe.py](../problems/molecular_biology-problems/rna_transcribe.py) replaces the three
former `rna_transcribe*` executables. Select one format and one direction mode:

| Options | Questions |
| --- | --- |
| `-m`, `--mc` | Multiple choice |
| `-f`, `--fib` | Fill in the blank |
| `-D`, `--directionless` | No prime labels; RNA bases align left-to-right with the template |
| `-p`, `--prime` | Prime labels; transcription respects strand direction |

```bash
source source_me.sh && python3 problems/molecular_biology-problems/rna_transcribe.py -m -p -d 5
source source_me.sh && python3 problems/molecular_biology-problems/rna_transcribe.py -f -D -s 12 -d 5
```

`-s/--sequence-length` (also `--seqlen`) sets DNA length; the default is 9 and the minimum is 2.
MC supports `-c/--num-choices` from 2 to 5 (default: 5). Output filenames include format,
direction mode, and length. Standard export and anti-cheat options remain available.
Prime FiB questions randomly use coding or template DNA and accept RNA in the 5' to 3' direction.
FiB accepts optional commas every three bases; prime mode also accepts direction labels.

[rna_transcribe_lib.py](../problems/molecular_biology-problems/rna_transcribe_lib.py) provides
`transcribe_sequence`, `fib_answers`, prompt/choice builders, and `generate_question` for reuse.

## Inputs and outputs

- Inputs: YAML/CSV/text reference data in [data/](../data/), YAML banks under
  [problems/matching_sets/](../problems/matching_sets/) and
  [problems/multiple_choice_statements/](../problems/multiple_choice_statements/),
  and images in [images/](../images/).
- Outputs (written to the repo root, ignored by git): Blackboard `bbq-*.txt`
  files, Blackboard `bez-*.zip` packages (and older `blackboard_export_zip-*.zip` files),
  QTI `qti*.zip` packages, and
  `selftest-*.html` previews.

## Known gaps

- [ ] Confirm which generators expose a `--dry-run` flag, if any.

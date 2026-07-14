# Biology problem generators

Standalone Python generators help biology instructors create randomized, LMS-ready quiz and homework questions across biochemistry, genetics, molecular biology, and related subjects.

Explore the generated question collection at
[Biology Problems OER](https://biologyproblems.org/).

## From concept to LMS-ready question

Choose a topic, run its generator, and receive questions ready for Blackboard or a QTI-compatible
learning management system. The current audited catalog covers 178 Python generators and 98 YAML
question banks, with standalone scripts for focused topics and shared tooling for consistent output.

For example, this command creates five randomized multiple-choice questions about hydrogen bonding
in an alpha-helix:

```bash
python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --mc -d 5
```

A generated question is printed in readable form while the import-ready version is written to disk:

```text
In a long alpha-helix, amino acid number 9 would form a hydrogen bond
with which two other amino acids?

A. amino acids 7 and 11
B. amino acids 6 and 12
C. amino acids 5 and 13
...

Writing 5 questions to file: bbq-alpha_helix_h-bonds-MC-questions.txt
```

The Blackboard output includes the question text, randomized answer choices, answer key, and the
HTML needed for LMS import.

## What you can create

- Generate multiple-choice, multiple-answer, and numeric questions from focused topic scripts.
- Cover biochemistry, biostatistics, cell biology, genetics, laboratory skills, and molecular
  biology from one repository.
- Export Blackboard text files, QTI packages, and HTML self-test previews.
- Build from Python logic, YAML matching sets, or statement-based question banks.
- Randomize scenarios and answer ordering so repeated assessments are less predictable.

## Quick start

### Prerequisites

- Python 3.12.
- The sibling
  [`qti-package-maker`](https://github.com/vosslab/qti-package-maker) repository cloned beside this
  repository.
- The packages listed in `pip_requirements.txt`.

The environment helper currently attempts to load the legacy
`qti-package-maker/source_me_for_testing.sh` helper, which is not present in the current sibling
repository. It may print a warning before continuing. See [docs/INSTALL.md](docs/INSTALL.md) for the
complete setup requirements.

### Generate your first questions

Clone both repositories into the same parent directory, then install the Python dependencies and
run a generator:

```bash
git clone https://github.com/vosslab/qti-package-maker.git
git clone https://github.com/vosslab/biology-problems.git
cd biology-problems
python3 -m pip install -r pip_requirements.txt
source source_me.sh
python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --mc -d 5
```

Successful generation prints each question, displays an answer-choice histogram, and creates
`bbq-alpha_helix_h-bonds-MC-questions.txt` in the repository root. The generated file is ignored by
Git and can be imported into Blackboard.

## Find a generator

- [docs/QUESTION_FUNCTION_INDEX.md](docs/QUESTION_FUNCTION_INDEX.md): Browse Python generators by
  subject, script, and question function.
- [docs/YAML_QUESTION_BANK_INDEX.md](docs/YAML_QUESTION_BANK_INDEX.md): Browse matching sets and
  statement banks backed by YAML.

Each generator is a standalone command. Run a script with `--help` to see its supported formats and
options:

```bash
python3 problems/biochemistry-problems/alpha_helix_h-bonds.py --help
```

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md): Prepare Python, dependencies, and sibling repositories.
- [docs/USAGE.md](docs/USAGE.md): Use common generator flags and understand generated artifacts.
- [docs/QUESTION_AUTHORING_GUIDE.md](docs/QUESTION_AUTHORING_GUIDE.md): Write and review a new
  question generator.
- [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md): Understand the generator-to-output data
  flow.
- [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md): Find generators, content banks, tools, and
  tests.

## Project status

The collection is actively maintained. The latest catalog audit recorded 178 Python generators and
98 YAML question banks across the supported biology subjects. Use the two indexes above for current
coverage and [docs/CHANGELOG.md](docs/CHANGELOG.md) for recent changes.

Platform support beyond macOS with Homebrew and exact minimum sibling-repository versions have not
yet been confirmed.

## License

Repository code is available under the
[GNU Lesser General Public License v3](LICENSE.LGPL_v3). Non-code educational content is available
under the
[Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/).

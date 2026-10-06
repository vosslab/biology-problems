# Question authoring guide

## Purpose

Use this guide to create a new question generator from scratch using
`TEMPLATE.py` as the starting point. It covers the required structure,
argparse setup, and output conventions used across this repo.

## Student-facing text

Design the puzzle first, then write the thinnest wrapper around it.

- Read [QUESTION_PEDAGOGY_GUIDE.md](QUESTION_PEDAGOGY_GUIDE.md) before writing code: it covers the
  data, the key, and the error-derived wrong choices.
- Read [QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md) before writing the stem and choices.
- Run [check_question_text.py](../devel/check_question_text.py) on the generated BBQ output. Its
  findings are advisory and point the item to a closer read.

## Start from `TEMPLATE.py`

- Copy `TEMPLATE.py` into the appropriate `problems/*-problems/` folder.
- Rename it using snake_case and a descriptive topic name.
- Keep the `#!/usr/bin/env python3` shebang and the `main()` entrypoint.

## Making `bptools` importable

Two simple options:

- Session-only: `source source_me.sh` (adds the repo root to `PYTHONPATH`).
- Editable install: `python3 -m pip install -e .`
  - This does not copy the code into `site-packages`.
  - It links to your working tree, so edits take effect immediately.

Example:

```bash
cp TEMPLATE.py problems/inheritance-problems/my_new_question.py
```

## Required structure

Your script should follow this shape, which matches the shared helpers:

- `get_question_text(...)` returns the prompt string; pass in any scenario values it needs.
- `generate_choices(num_choices, ...)` returns `(choices_list, answer_text)`, built from the same
  scenario values as the prompt.
- `write_question(N, args)` returns the formatted question string.
- `parse_arguments()` builds an argparse parser with shared helpers.
- `main()` creates the output name and calls
  `bptools.collect_and_write_questions(write_question, args, outfile)`.

Minimal skeleton (tabs for indentation):

```python
#!/usr/bin/env python3

import bptools

def get_question_text() -> str:
	question_text = "You add 10 &micro;L of stock solution to 90 &micro;L of distilled water. "
	question_text += "What fraction of the new solution is stock solution?"
	return question_text

def generate_choices(num_choices: int) -> (list, str):
	answer_text = "1/10"
	# choices stay in natural order (numbers ascending), so there is no shuffle
	choices_list = [
		answer_text,
		# error: divides the stock volume by the water volume, not the total (10/90)
		"1/9",
		# error: reports the water fraction instead of the stock fraction (90/100)
		"9/10",
	]
	return choices_list, answer_text

def write_question(N: int, args) -> str:
	question_text = get_question_text()
	choices_list, answer_text = generate_choices(args.num_choices)
	complete_question = bptools.formatBB_MC_Question(
		N,
		question_text,
		choices_list,
		answer_text,
	)
	return complete_question
```

Derive each wrong choice from one named student error and keep the error comment; `TEMPLATE.py`
computes its wrong choices in code. Shuffle only choices that have no natural order (see Layout
and order in [QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md)).

## Argparse setup

Use shared bundles so CLI flags are consistent across generators:

- `bptools.make_arg_parser(...)` for base args (`-d/--duplicate-runs`, etc.).
- `bptools.add_choice_args(parser)` for `-c/--num-choices`.
- `bptools.add_hint_args(parser)` when a hint mode is supported.
- `bptools.add_question_format_args(parser, required=True)` if the script can
  emit multiple formats (MC, FIB, etc.).

Keep both short and long flags for any new arguments you add.

## Output file naming

Use `bptools.make_outfile(...)` to keep output names predictable. Typical parts:

- `args.question_type.upper()` for the format
- `with_hint` or `no_hint` if hinting is supported
- `f"{args.num_choices}_choices"` for MC/MA formats

Example:

```python
outfile = bptools.make_outfile(
	args.question_type.upper(),
	hint_mode,
	f"{args.num_choices}_choices"
)
```

Generated files like `bbq-*.txt` should not be committed.

## Style guardrails

- Use tabs for Python indentation.
- Keep comments ASCII-only and on their own line.
- Prefer f-strings and simple return statements.
- Avoid `import *`, avoid heredocs, and avoid environment variables for config.
- Keep line length under 100 characters when practical.

## Blackboard HTML and JavaScript sanitization

Blackboard aggressively rewrites HTML/JS and can inject whitespace inside
JavaScript function tokens. When embedding JavaScript in bptools-generated
HTML, keep function declarations tightly controlled and use the split-comment
pattern already used in PUBCHEM generators to prevent Blackboard from
rewriting whitespace. Example patterns seen in this repo include:

- `function/* */handlerName()` (breaks the keyword to avoid sanitizer edits)
- `sub/* */function_name()` (legacy pattern kept for compatibility)

Do not "clean up" these comment splits unless you have verified Blackboard
renders the script correctly after the change.

## Testing and sanity checks

Run the script with a small duplicate count and choices count:

```bash
source source_me.sh && python3 problems/inheritance-problems/my_new_question.py --mc -d 1 -c 4
```

Cover pure helper functions that deserve protection with a pytest file in `tests/`. Asserts live
only in `tests/`, never in generator scripts (see [PYTHON_STYLE.md](PYTHON_STYLE.md) and
[PYTEST_STYLE.md](PYTEST_STYLE.md)).

## Changelog

Document any new generator or doc update in `docs/CHANGELOG.md` with the
current date.

# Unification plan

## Purpose
- Make generator scripts easier to read and maintain while preserving current CLI behavior.
- Reduce copy/paste in `main()` and argument parsing.
- Keep per-script question logic clear and local.

## Scope
- Standardize how scripts collect questions with `-d/--duplicate-runs` (alias
  `--duplicates`) and `-x/--max-questions`.
- Provide a shared way to add base CLI args while allowing custom flags.
- Migrate incrementally; no mass refactor required.

## Principles
- Prefer small helper functions over base classes.
- Keep script-specific logic in plain functions, not hidden in inheritance.
- Avoid lambdas; use direct function references.
- Preserve existing CLI semantics and output filenames.

## Decision points

### Shortfall behavior
- If `-x/--max-questions` is not reached after `-d/--duplicate-runs` (alias
  `--duplicates`) attempts, helpers return the smaller set and print a warning
  (for example, "generated 87 of 99 after 110 attempts"). This avoids silent
  shortfalls.

### Return contracts
- Single-question writers: `write_question(N, args)` returns a non-empty string
  or `None`. `None` means "no question generated." Empty strings are invalid and
  should be skipped with a warning.
- Batch writers: `write_question_batch(N, args)` returns a list of non-empty
  strings. An empty list means "no questions this attempt." The list must not
  contain `None` values.

### Output newline policy
- Each emitted question string must be a single line and end with `\\n`.
- Helpers may append a trailing newline if missing.
- If a question contains internal newlines (after trimming the final `\\n`),
  helpers should warn and skip the question.

### Argparse composition
- `parse_arguments()` should call `add_base_args(parser)` first, then add custom
  flags. This keeps `-d/--duplicate-runs` (alias `--duplicates`) and
  `-x/--max-questions` consistent across scripts.
- Recommended default help text:
  - `-d/--duplicate-runs`: "Number of duplicate runs (attempts) to generate questions."
  - `-x/--max-questions`: "Maximum number of questions to keep."
- Defaults remain `duplicates=2` and `max_questions=None` unless a script
  explicitly needs different values.

### Direct-to-file legacy scripts
- Scripts that write inside loops should be converted to return lists and use
  helpers, but only when the script is otherwise being edited.

## Proposed helpers

### Question collection helpers
Two helpers cover the main cases without a separate normalize step.
Both treat `-d/--duplicate-runs` (alias `--duplicates`) as attempts and
`-x/--max-questions` as a hard cap.
Both preserve a stable `N` that only advances when a question is accepted.
Writers should accept the full `args` namespace for consistency.

- `collect_questions(write_question, args)`
  - Use when `write_question(N, args)` returns a single question string or `None`.
  - Enforces `-d` attempts and caps at `-x` questions.
  - Passes `N` as the next successful question number (1-based).

- `collect_question_batches(write_question_batch, args)`
  - Use when a generator produces multiple questions per attempt.
  - Expects `write_question_batch(N, args)` to return a list of question strings.
  - Enforces `-d` attempts and caps at `-x` questions.
  - Passes `N` as the starting question number for the batch and advances by the
    number of accepted questions.

### Output helpers
- `make_outfile(script_path=None, *parts)`
  - Builds `bbq-<script>-<parts>-questions.txt` while skipping empty parts.
  - Uses `sys.argv[0]` when `script_path` is omitted.
- `collect_and_write_questions(write_question, args, outfile)`
  - Convenience helper that calls `collect_questions(...)` and writes the output.
  - Standardizes status messages and pluralization.

### Batch script defaults
- Batch generators that return large fixed lists should set
  `max_questions_default=99` when calling `add_base_args(...)`.
- Keep the global default `duplicate_runs=2` for quick testing.

### Histogram printing
Helpers may print the answer histogram when MC/MA questions are present, instead
of relying on CLI flags. The detection rule should be simple and consistent:

- If any emitted question string starts with `MC` or `MA` (for example `MC\t`),
  call `bptools.print_histogram()`.

### Common CLI args
Add a shared function that scripts can opt into:

- `add_base_args(parser)`
  - Adds `-d/--duplicate-runs` (alias `--duplicates`) and `-x/--max-questions`.
  - Returns the parser so scripts can chain custom arguments.

This keeps scripts consistent while still allowing custom flags and defaults.

### Parser helper
Use a helper to avoid repeating parser construction and base args:

- `make_arg_parser(description=None, batch=False)`
  - Creates an `argparse.ArgumentParser` and applies base args.
  - When `batch=True`, uses batch defaults (`duplicate_runs=2`, `max_questions=99`).

### Batch CLI args
Use a batch-specific helper so large fixed lists are capped by default:

- `add_base_args_batch(parser)`
  - Same flags as `add_base_args(...)`.
  - Defaults to `duplicate_runs=2` and `max_questions=99`.

### Optional CLI helpers
These can be added later to reduce boilerplate, without forcing all scripts to
adopt them at once.

- `add_choice_args(parser)`
  - Adds `-c/--num-choices` with a standard help string and default.

- `add_hint_args(parser)`
  - Adds `--hint` and `--no-hint` with a standard default.

- `add_question_format_args(parser, types_list=None)`
  - Adds `--format` with allowed types from `types_list`.
  - Adds long flags for requested types: `--mc`, `--ma`, `--num`, and `--fib`.
  - Adds expanded aliases: `--multiple-choice`, `--multiple-answer`,
    `--numeric`, and `--fill-in-blank`.

- `add_difficulty_args(parser)`
  - Adds `--difficulty` and `--easy/--medium/--rigorous` shortcuts.

- `add_output_args(parser)`
  - Optional `--outfile` override for scripts that want it.
  - Scripts that do not use `--outfile` keep their current naming rules.

- `add_format_args(parser)`
  - Only for scripts that truly need a question format flag.
  - Most scripts can infer MC/MA from emitted strings and avoid this arg.

## Example usage
Single-question generators:

- `write_question(N, args) -> str | None`
- `questions = collect_questions(write_question, args)`

Batch generators:

- `write_question_batch(N, args) -> list[str]`
- `questions = collect_question_batches(write_question_batch, args)`

## Migration plan

### Phase 1: Document and prototype
- Add helpers to `bptools.py`.
- Update `TEMPLATE.py` to demonstrate the new flow.
- Convert 2-3 representative scripts to validate the pattern.

### Phase 2: Gradual adoption
- Convert scripts as they are touched for content updates.
- Favor high-duplication scripts first (largest maintenance win).
- Keep diffs small and focused.

### Phase 3: Special-case tooling
- Review YAML-driven tools in `multiple_choice_statements/` and `matching_sets/`.
- Decide if they adopt the helpers or keep their bespoke pipelines.

## Known special cases
- YAML-driven tools that batch-generate across many files may keep their own flow.
- Scripts that write directly to file inside loops can move to list returns over
  time when convenient.

## Open questions
- Should helpers accept a `start_index` override for special cases?
- Should histogram printing be toggled by a helper flag or always auto-detected?

# Unification plan

## Purpose
- Make generator scripts easier to read and maintain while preserving current CLI behavior.
- Reduce copy/paste in `main()` and argument parsing.
- Keep per-script question logic clear and local.

## Scope
- Standardize how scripts collect questions with `-d/--duplicates` and
  `-x/--max-questions`.
- Provide a shared way to add base CLI args while allowing custom flags.
- Migrate incrementally; no mass refactor required.

## Principles
- Prefer small helper functions over base classes.
- Keep script-specific logic in plain functions, not hidden in inheritance.
- Avoid lambdas; use direct function references.
- Preserve existing CLI semantics and output filenames.

## Proposed helpers

### Question collection helpers
Two helpers cover the main cases without a separate normalize step.

- `collect_questions(write_question, args)`
  - Use when `write_question(...)` returns a single question string or `None`.
  - Enforces `-d` attempts and caps at `-x` questions.

- `collect_question_batches(write_question_batch, args)`
  - Use when a generator produces multiple questions per attempt.
  - Expects `write_question_batch(...)` to return a list of question strings.
  - Enforces `-d` attempts and caps at `-x` questions.

### Common CLI args
Add a shared function that scripts can opt into:

- `add_base_args(parser)`
  - Adds `-d/--duplicates` and `-x/--max-questions`.
  - Returns the parser so scripts can chain custom arguments.

This keeps scripts consistent while still allowing custom flags and defaults.

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
- Which defaults should `add_base_args(parser)` use for `-d` and `-x`?
- Should batch helpers accept a `start_index` to preserve existing numbering?
- Should histogram printing be part of helpers or remain in `main()`?

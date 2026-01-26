# HTML to WeBWorK Plan (PGML Output)

## Scope
- Translate HTML-ish content from YAML and generators into PGML-safe output.
- Web rendering only unless a specific problem requires hardcopy support.

## Non-goals
- Do not emit raw HTML tables in PGML output.
- Do not rely on MathJax for styling or coloring.
- Do not add "smart" parsing inside PG/PGML.

## Hard constraints in this install
- HTML tables (`table`, `tr`, `td`) are blocked and must not be emitted.
- Use PGML for structure and PGML tag wrappers for allowed HTML (`span`, `div`).
- PGML parses once; it will not re-parse PGML tag wrapper syntax constructed inside Perl variables.

## Pipeline contract (generator responsibilities)
- Sanitization and conversion happen in Python, not in PG.
- Table detection and warnings live in the generator.
- Output PGML should be flat and deterministic.

## Translation rules (high level)
- `span style="color: ..."` -> HTML span with CSS class (preferred) or inline style (fallback), then output with `[$var]*` if stored in a variable.
- `<sub>`/`<sup>` -> Unicode conversion (digits and common signs; Greek baseline).
- `<table>` -> translate via niceTables.pl or drop with a warning (see table plan).
- All other unsupported HTML tags -> strip to plain text.

## Link map
- Replacement rules: [REPLACEMENT_RULES_IMPLEMENTATION_PLAN.md](REPLACEMENT_RULES_IMPLEMENTATION_PLAN.md)
- Color classes: [COLOR_CLASS_MIGRATION_PLAN.md](COLOR_CLASS_MIGRATION_PLAN.md)
- Color usage patterns: [COLOR_TEXT_IN_WEBWORK.md](COLOR_TEXT_IN_WEBWORK.md)
- Table translation: [NICETABLES_TRANSLATION_PLAN.md](NICETABLES_TRANSLATION_PLAN.md)

## Decision: YAML tables
- Drop the four YAML tables and move on.
- The generator will continue to treat table content as a special case and skip
  risky conversions when `<table`, `<tr`, or `<td>` appears.

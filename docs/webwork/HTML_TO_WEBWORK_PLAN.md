# HTML to WeBWorK Plan (PGML Output)

## Scope
- Translate HTML-ish content from YAML and generators into PGML-safe output.
- Web rendering only; use MODES only when HTML must be emitted from Perl.

## Non-goals
- Do not emit raw HTML tables in PGML output.
- Do not rely on MathJax for styling or coloring.
- Do not add "smart" parsing inside PG/PGML.

## Hard constraints in this install
- HTML tables (`table`, `tr`, `td`, `th`) are blocked and must not be emitted.
- Use PGML for structure. For inline HTML, use PGML tag wrappers or raw HTML passed through with `*`. For layout in PG 2.17, use `MODES(...)` wrappers only when HTML must be emitted from Perl.
- PGML parses once; it will not re-parse PGML tag wrapper syntax constructed inside Perl variables.

## Pipeline contract (generator responsibilities)
- Sanitization and conversion happen in Python, not in PG.
- Table detection and warnings live in the generator.
- Output PGML should be flat and deterministic.

## Translation rules (high level)
- `span style="color: ..."` -> HTML span with inline style (current default), then output with `[$var]*` if stored in a variable. Class-based spans are a future option.
- `<sub>`/`<sup>` -> Unicode conversion (digits and common signs; Greek baseline).
- `<table>` -> translate via niceTables.pl or drop with a warning (see table plan). niceTables is the only supported path for tables because it avoids the blocked tags.
- All other unsupported HTML tags -> strip to plain text.

## Link map
- Replacement rules: [REPLACEMENT_RULES_IMPLEMENTATION_PLAN.md](REPLACEMENT_RULES_IMPLEMENTATION_PLAN.md)
- Color classes: [COLOR_CLASS_MIGRATION_PLAN.md](COLOR_CLASS_MIGRATION_PLAN.md)
- Color usage patterns: [COLOR_TEXT_IN_WEBWORK.md](COLOR_TEXT_IN_WEBWORK.md)
- Table translation: [NICETABLES_TRANSLATION_PLAN.md](NICETABLES_TRANSLATION_PLAN.md)

## Decision: YAML tables
- Convert YAML tables to niceTables output (no more skipping table content).
- The generator should treat table content as a special case and route it to
  the niceTables converter when `<table`, `<tr`, `<td`, or `<th>` appears.
- If the table shape is unsupported, log a warning and keep the content for
  manual rewrite rather than dropping it silently.

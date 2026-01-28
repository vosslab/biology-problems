# Matching Problems: Legacy vs Modern PGML

## Summary

**UPDATE 2026-01-24:** Matching PGML uses HTML layout wrappers in this repo. The matching generator ([problems/matching_sets/yaml_match_to_pgml.py](../../problems/matching_sets/yaml_match_to_pgml.py)) follows the `matching_from_web.pgml` pattern using `MODES(...)` wrappers to build a flexbox HTML layout.

## Recommended pattern (HTML-only output)

Use PopUp widgets from `parserPopUp.pl` (DropDown is PG 2.18+) and `MODES(...)` wrappers when HTML must be emitted from Perl. For forward compatibility, you can wrap widget creation to prefer `DropDown` when available and fall back to `PopUp`. Keep matching data as plain text plus TeX math when needed for MathJax, and add color only at render time.

```perl
loadMacros(
  "PGstandard.pl",
  "PGML.pl",
  "parserPopUp.pl",
  "PGcourse.pl",
);

# ... build @q_and_a, @answers, @shuffle, @answer_dropdowns ...

HEADER_TEXT(MODES(HTML => <<END_STYLE));
<style>
.two-column {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  align-items: center;
  justify-content: space-evenly;
}
</style>
END_STYLE

BEGIN_PGML
Match each question with its answer.

[@ MODES(HTML => '<div class="two-column"><div>') @]*
[@ join(
  "\n\n",
  map {
    '[_]{$answer_dropdowns[' . $_ . ']} '
      . '*' . ($_ + 1) . '.* '
      . $q_and_a[$_][0]
  } 0 .. $#q_and_a
) @]**
[@ MODES(HTML => '</div><div>') @]*
[@ join(
  "\n\n",
  map {
    '*' . $ALPHABET[($_)] . '.* ' . $answers[$shuffle[$_]]
  } 0 .. $#answers
) @]**
[@ MODES(HTML => '</div></div>') @]*
END_PGML
```

Notes:

- Use `MODES(...)` for HTML-only styling blocks or layout wrappers that PGML would otherwise escape.
- MODES is only needed when the wrapper HTML must be emitted from Perl (for
  example inside `[@ ... @]*` blocks between the joined columns). If you remove
  MODES without moving the HTML into plain PGML, the wrapper tags may be escaped
  or omitted, collapsing the layout into a single column.
- If you can place the wrapper tags directly in PGML, prefer plain HTML and
  avoid MODES entirely.
- PGML parses once. Do not build PGML tag wrappers inside Perl variables and expect a second parse.
- If YAML uses HTML entities (named or numeric), the generator unescapes them into Unicode characters so they render without MathJax. `<sub>`/`<sup>` tags are converted into Unicode subscripts/superscripts before other HTML is stripped.
- For fixed label colors, build HTML labels in Perl (for example `%answer_html`) and emit them with `[$answers_html[$shuffle[$_]]]*` so spans survive PGML escaping. See [COLOR_TEXT_IN_WEBWORK.md](COLOR_TEXT_IN_WEBWORK.md).
- Right-column labels can be formatted as `*A.*` (bold) or `A\.` (escaped dot). Plain `A.` may be parsed as an ordered list marker depending on context.
- Default output uses inline HTML spans for replacement-rule colors. Use `--no-color` to disable styling; `--use-colors` is an explicit enable (same as default).

## HTML whitelist and layout constraints

This install blocks several HTML tags inside PGML, including `table`, `tr`, `td`, and `th`. Those tags trigger PGML warnings and render garbage.

Preferred layout options:

- Two columns: use flexbox with `div` wrappers.
- Table-like grids: use `niceTables.pl`. It is the only supported way to create tables because it avoids the blocked HTML table tags.
- Small styling: `span` is usually allowed.

If a sanitizer strips `<style>` blocks (for example in Blackboard), fall back to inline styles on elements, or use `<font color="...">` as a last resort.

## Legacy pattern (historical)

Older matching problems use `PGchoicemacros.pl` and `ColumnMatchTable($ml)` with a separate `ANS(...)` call. That still works, but it is legacy style and triggers PGML linter warnings for mixed style.

## Document history

- 2026-01-24: Updated guidance with PGML tag-wrapper layout and HTML whitelist constraints.
- 2026-01-28: Clarified that matching layouts use HTML wrappers in this repo.
- 2026-01-21: Initial documentation of matching problems and legacy patterns.

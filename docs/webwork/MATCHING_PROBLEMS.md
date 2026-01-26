# Matching Problems: Legacy vs Modern PGML

## Summary

**UPDATE 2026-01-24:** Matching PGML is dual output (HTML and TeX). The matching generator ([problems/matching_sets/yaml_match_to_pgml.py](../../problems/matching_sets/yaml_match_to_pgml.py)) now follows the `matching_from_web.pgml` pattern using `MODES(...)` wrappers to build a flexbox HTML layout while keeping TeX wrappers present.

## Recommended pattern (PGML dual output)

Use DropDown widgets from `parserPopUp.pl` and `MODES(...)` wrappers so both HTML and TeX slots exist. Keep matching data as plain text plus TeX math, and add color only at render time.

```perl
loadMacros(
  "PGstandard.pl",
  "PGML.pl",
  "parserPopUp.pl",
  "PGcourse.pl",
);

# ... build @q_and_a, @answers, @shuffle, @answer_dropdowns ...

HEADER_TEXT(MODES(TeX => '', HTML => <<END_STYLE));
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

[@ MODES(TeX => '\\parbox{0.4\\linewidth}{',
  HTML => '<div class="two-column"><div>') @]*
[@ join(
  "\n\n",
  map {
    '[_]{$answer_dropdowns[' . $_ . ']} '
      . '*' . ($_ + 1) . '.* '
      . $q_and_a[$_][0]
  } 0 .. $#q_and_a
) @]**
[@ MODES(TeX => '}\\hfill\\parbox{0.4\\linewidth}{',
  HTML => '</div><div>') @]*
[@ join(
  "\n\n",
  map {
    '*' . $ALPHABET[($_)] . '.* ' . $answers[$shuffle[$_]]
  } 0 .. $#answers
) @]**
[@ MODES(TeX => '}', HTML => '</div></div>') @]*
END_PGML
```

Notes:

- Keep the TeX wrapper slots present, even if you never print hardcopy.
- Use `MODES(TeX => '', HTML => ...)` for HTML-only styling blocks.
- Avoid raw HTML in YAML matching data. The generator strips tags to prevent PGML whitelist issues. If you need color without MathJax, use CSS on the right column (for example `:nth-child()` selectors) rather than per-item spans.
- If YAML uses HTML entities (named or numeric), the generator unescapes them into Unicode characters so they render without MathJax. `<sub>`/`<sup>` tags are converted into Unicode subscripts/superscripts before other HTML is stripped.
- Right-column labels must not use `*A.*` (bold-list markup). In this install, `A.` is parsed as an ordered list marker, so emit `A\.` (escaped dot) to force plain text labels.
- Use `--use-colors` to bake MathJax-colored choice labels into the generated PG. When enabled, the generator rewrites the choice keys into PGML math strings like `[\color{#HEX}{\text{label}}]` using the qti color wheel palette and disables CSS nth-child coloring to avoid double styling.

## HTML whitelist and layout constraints

This install blocks several HTML tags inside PGML, including `table`, `tr`, and `td`. Those tags trigger PGML warnings and render garbage.

Preferred layout options:

- Two columns: use flexbox with `div` wrappers.
- Table-like grids: use a TeX `array` (renders via MathJax in HTML), or `niceTables.pl` if that macro is available.
- Small styling: `span` is usually allowed.

If a sanitizer strips `<style>` blocks (for example in Blackboard), fall back to inline styles on elements, or use `<font color="...">` as a last resort.

## Legacy pattern (historical)

Older matching problems use `PGchoicemacros.pl` and `ColumnMatchTable($ml)` with a separate `ANS(...)` call. That still works, but it is legacy style and triggers PGML linter warnings for mixed style.

## Document history

- 2026-01-24: Updated guidance with PGML tag-wrapper layout, empty TeX placeholders, and HTML whitelist constraints.
- 2026-01-21: Initial documentation of matching problems and legacy patterns.

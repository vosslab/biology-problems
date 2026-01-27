# PGML Linter Notes: Expectation vs Rendered Output

This note documents common cases where our PGML expectations did not match
renderer output, and the checks a linter can do to catch them early.

## Mismatch: PGML is single-pass

Expectation:
- Build PGML tag wrapper syntax inside Perl strings and have PGML parse it.

What actually happens:
- PGML parses once. Tag wrappers embedded in Perl variables are not re-parsed.
- Result: literal `[<...>]{[...]}` text or parser errors.

Linter checks:
- Warn when strings assigned in Perl contain `"[<` or `]{[` patterns.
- Error when `[$... ]` PGML interpolation appears inside a `[@ ... @]` eval block
  (PGML will not re-parse it).
- Warn when variables containing `<span` are rendered without trailing `*` in PGML.

## Mismatch: HTML in variables gets escaped

Expectation:
- Store `<span style="...">` in a Perl variable and print it with `[$var]`.

What actually happens:
- PGML escapes the HTML unless you use the raw pass-through `*`.

Linter checks:
- If a variable likely contains HTML (`<span`, `<div>`, `<sup>`, `<sub>`) and is
  output as `[$var]` (no trailing `*`), warn.
- Suggest `[$var]*`.

## Mismatch: MODES(...) inside eval blocks

Expectation:
- Use `MODES(TeX => '', HTML => '<div>...')` inside `[@ ... @]` to emit HTML.

What actually happens:
- `MODES(...)` returns `1` in eval context; you get `1` rendered instead of HTML.

Linter checks:
- Warn when `MODES(` appears inside a `[@ ... @]` block.
- Recommend using PGML tag wrappers or raw HTML outside eval blocks.

PG 2.17 exception:
- For two-column matching layouts, we intentionally use
  `MODES(TeX => '', HTML => '<div ...>')` inside `[@ ... @]` to emit raw HTML.
  In this repo, treat that pattern as allowed (warn at most) because the
  PG 2.17 renderer requires it for stable layout.

## Mismatch: MathJax color does not render

Expectation:
- `[\color{#hex}{\text{...}}]` or `\textcolor{}` colors text.

What actually happens:
- MathJax does not process injected TeX in our install; backslashes are wrapped
  in `tex2jax_ignore` spans and color never renders.

Linter checks:
- Warn when `\color{` or `\textcolor{` appears in PGML text.
- Recommend HTML span styling instead.

## Mismatch: HTML whitelist blocks tables

Expectation:
- Raw `<table>`, `<tr>`, `<td>` output renders.

What actually happens:
- These tags are blocked; output is stripped or triggers PGML warnings.

Linter checks:
- Error on `<table`, `<tr`, `<td` in PGML output.
- Suggest `niceTables.pl` or flexbox `div` layout.

PG 2.17 exception:
- Allow `<div>` and `<span>` in PGML output when emitted through HTML-only
  `MODES(TeX => '', HTML => ...)` wrappers. This is the recommended pattern in
  `WEBWORK_PROBLEM_AUTHOR_GUIDE.md` for matching layouts.

## Mismatch: Ordered list auto-parsing

Expectation:
- Right-column labels like `A.` are rendered as plain text.

What actually happens:
- PGML sometimes parses `A.` as list markup.

Linter checks:
- Warn on `A.` or `B.` patterns used as labels in PGML text.
- Suggest `*A.*` (bold) or `A\.` (escaped dot).

## Mismatch: Renderer API lint returns non-JSON

Expectation:
- Renderer returns JSON with lint findings.

What actually happens:
- When the renderer is down or returns HTML, the client gets JSON decode errors.

Linter checks:
- If response body is empty or starts with `<`, report "renderer not running"
  or "non-JSON response" with the base URL.

## Quick smoke checks (static)

- PGML tag wrappers inside Perl variables: `"[<"`, `"]{["`.
- HTML in variables without `*`: `[$var]` with `<span` in value.
- `MODES(` inside `[@ ... @]` eval blocks.
- TeX color macros: `\\color{`, `\\textcolor{`.
- Blocked tags: `<table`, `<tr`, `<td>`.
- Ordered list label patterns: `A.` / `B.` in right-column text.

## Additional checks for poorly formed PGML

### Structural PGML
- Missing `DOCUMENT();` or `ENDDOCUMENT();`.
- Unmatched `BEGIN_PGML` / `END_PGML` blocks.
- Nested `BEGIN_PGML` without closing.
- Unbalanced `[@ ... @]` eval blocks.

### HTML whitelist hazards
- `<style>` blocks outside `HEADER_TEXT(MODES(TeX => '', HTML => ...))`.
- Disallowed tags inside PGML tag wrappers (install whitelist).

### MathJax color failures
- `\\color{` or `\\textcolor{` in PGML output (warn: likely ignored).

### List parsing traps
- Right-column labels like `A.` or `B.` in plain text (suggest `*A.*` or `A\\.`).

### Encoding and mojibake
- Replacement character `�`.
- Common mojibake patterns: `Â`, `Ã`, `â€™`, `â€“`, `â€”`, `â€¢`.
- Non-printable control characters (ASCII 0x00-0x1F excluding `\n`, `\r`, `\t`).

### Macro/widget sanity
- `DropDown(...)` used without `parserPopUp.pl` in `loadMacros`.
- `RadioButtons(...)` used without `parserRadioButtons.pl`.
- `NchooseK(...)` used without `PGchoicemacros.pl`.

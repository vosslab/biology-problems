# Replacement Rules Implementation Plan (PGML Matching Sets)

## Goals
- Preserve the semantic intent of existing `replacement_rules`.
- Keep PGML output compatible with this install's HTML whitelist.
- Avoid risky auto-conversions by requiring strict patterns or explicit opt-in.

## Processing order (current + planned)
1. Apply `replacement_rules` to raw text (existing behavior).
2. Convert `<sub>`/`<sup>` to Unicode.
3. Strip remaining HTML tags.
4. Unescape HTML entities.
5. Normalize non-breaking spaces to plain spaces.

## Subscript and superscript handling
- Convert digits and common signs inside `<sub>`/`<sup>` to Unicode.
- Map available letter subscripts where Unicode exists.
- For Greek in subscripts (for example `C<sub>&alpha;</sub>`), use baseline Greek:
  `C<sub>&alpha;</sub>` -> `C alpha` (alpha on baseline).
- Normalize `&ndash;` and Unicode minus variants to `-` inside `<sup>`/`<sub>`.

## Table guard (required)
- If a string contains `<table`, `<tr`, or `<td>`, skip any color conversion.
- Apply only the safe sanitize path (sub/sup, unescape, strip tags).
- Log a warning so the entry can be cleaned up later.

## Color handling

### Default (safe, legacy)
- Preserve existing inline color spans after replacement rules.
- When strict parsing succeeds, convert to HTML spans and emit through `[$var]*`
  when the text is stored in Perl arrays or variables.

### Future: strict class mode (opt-in)
- Only convert when the rule matches a strict pattern:
  - A single `<span>` with a `color:` style and no other nested tags.
  - Optional `<strong>` wrapper allowed; translate to `font-weight:700`.
- Accept either hex colors or named colors, and tolerate unquoted `style=color: ...`.
- Extract the color value and generate a CSS class.
- Emit HTML spans (class-based or inline), and pass them through with `*` when
  the content lives in Perl variables (PGML does not re-parse tag wrappers built in Perl).
- If any rule does not match the strict pattern, leave it untouched and log a warning.

## Bold and italic (pending)
- Current plan: strip `<strong>`, `<b>`, `<em>`, `<i>` to plain text.
- Future option (opt-in): map `<strong>` to a CSS class (font-weight),
  and map `<em>` to a class (font-style) when strict conversion is enabled.
  This should only apply inside strict color-class conversion blocks.

## HTML entities and spacing
- Unescape entities after sub/sup conversion so `&chi;`, `&alpha;`, `&times;` survive.
- Normalize `&nbsp;` and unicode NBSP to plain spaces to avoid layout surprises.

## Warnings and visibility
- Log warnings for:
  - Table content detected (conversion skipped).
  - Non-strict color spans when strict conversion is requested in the future.
  - Unsupported HTML tags encountered in replacement output.

## Migration strategy
- Keep YAML stable now.
- Add new explicit `color_rules` only when editing a file.
- Prefer small, local changes over a repo-wide refactor.

## Implemented flags (current)
- Default coloring is inline spans derived from strict `<span style="color: ...">` rules.
- `--no-color` disables coloring.
- `--use-colors` is an explicit enable (same as default).

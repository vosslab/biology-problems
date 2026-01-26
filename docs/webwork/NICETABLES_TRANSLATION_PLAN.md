# niceTables Translation Plan (HTML Tables to PGML)

## Purpose
Define how HTML table content should be translated into WeBWorK outputs using
niceTables.pl so that blocked HTML tags are avoided.

## Table types (choose the correct target)
- Data tables: use `DataTable()` (semantic data with headers or captions).
- Layout tables: use `LayoutTable()` (visual layout without HTML table output).

## Supported input shapes
- 2D arrays of cell content.
- Cell content can be:
  - plain text
  - hashref with `data => ...` and per-cell options
  - arrayref where item 0 is content followed by key/value options

## Table-level options to support first
Start with a minimal option set:
- `center`
- `caption` (DataTable only)
- `horizontalrules`
- `valign`
- `padding`
- CSS hooks: `tablecss`, `datacss`, `headercss`, `allcellcss`, `columnscss`

## PGML table syntax (optional)
PGML supports table syntax using `[# ... #]` which is backed by niceTables.
This is acceptable for generator output when it improves readability.

## Translation approach for HTML tables

### Phase 1 supported subset
- `<table><tr><td>` only
- no nested tables
- no `rowspan` or `colspan`
- optional `<th>` for header cells

### Mapping rules
- If a header row or caption intent is detected, use `DataTable()`.
- If content is purely layout (two-column lists, widget grids), use `LayoutTable()`.

### Out-of-scope tables
- Do not emit raw HTML.
- Log a warning and fall back to plain text or require manual rewrite.

## Implementation notes
- Keep table detection in Python.
- Avoid parsing HTML beyond the supported subset.
- Maintain a warning list so failures are visible in generator output logs.

## Validation
- Add a small PGML table probe problem to check:
  - no blocked HTML tags in output
  - layout readability on narrow screens
  - consistent styling with CSS classes

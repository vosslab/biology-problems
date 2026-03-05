# niceTables Translation Plan (HTML Tables to PGML)

## Purpose
Define how HTML table content should be translated into WeBWorK outputs using
niceTables.pl so that blocked HTML table tags are avoided. This is the only
supported way to create tables in this install.

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
- Log a warning and require manual rewrite (do not silently drop table content).

## Implementation notes
- Keep table detection in Python.
- Avoid parsing HTML beyond the supported subset.
- Maintain a warning list so failures are visible in generator output logs.

## Per-row styling with cellcss

niceTables supports per-cell `cellcss` for alternating row colors and custom formatting.
Apply the same CSS string to every cell in a row to get row-level styling.

```perl
# Build data rows with alternating background colors
my @data_rows = ();
for my $row_num (0 .. $#data) {
    # alternate between pale yellow and white
    my $bg = ($row_num % 2 == 0) ? '#FFFFDD' : '#FFFFFF';
    my $row_css = "background:$bg;font-family:courier,monospace;"
        . "text-align:right;padding:4px 10px;";
    push @data_rows, [
        [ $data[$row_num][0], cellcss => $row_css ],
        [ $data[$row_num][1], cellcss => $row_css ],
    ];
}

$table = LayoutTable(
    [ @header_row, @data_rows ],
    center => 1,
    allcellcss => 'padding:4px 10px;',
);
```

Key points:
- `cellcss` is set per cell, not per row. Repeat the same CSS for each cell in a row.
- This pattern works with both `DataTable()` and `LayoutTable()`.
- Use `allcellcss` for table-wide defaults and `cellcss` for per-cell overrides.

**Working example:** `michaelis_menten_table_km.pgml`

## Validation
- Add a small PGML table probe problem to check:
  - no blocked HTML tags in output
  - layout readability on narrow screens
  - consistent styling with CSS classes

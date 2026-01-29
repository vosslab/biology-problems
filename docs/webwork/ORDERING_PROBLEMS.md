# Ordering Problems (DraggableProof)

This guide describes how to build ordering (rank/sequence) questions in PGML
using the `draggableProof.pl` widget.

## When to use

Use `DraggableProof` when students must place items into a correct order. It
provides a drag-and-drop interface with automatic checking.

## Required macros

Include the macros below in the preamble:

```perl
loadMacros(
  "PGstandard.pl",
  "MathObjects.pl",
  "PGML.pl",
  "draggableProof.pl",
  "PGcourse.pl",
);
```

## PGML pattern

Build the widget in a Perl block, then inject the rendered HTML into PGML with
`[$var]*`. The inline `[_]{$ordering}` pattern does not work with the current
PG 2.17 renderer in this repo.

```perl
DOCUMENT();

loadMacros(
  "PGstandard.pl",
  "MathObjects.pl",
  "PGML.pl",
  "draggableProof.pl",
  "PGcourse.pl",
);

@ordered_items = (
  "Option 1",
  "Option 2",
  "Option 3",
);

$ordering = DraggableProof(
  [@ordered_items],
  [],
  SourceLabel => "Options",
  TargetLabel => "Rank in order of increasing property",
  DamerauLevenshtein => 1,
);
$ordering_html = $ordering->Print;

BEGIN_PGML
Arrange the options in order.

[$ordering_html]*
END_PGML

ANS($ordering->cmp);

ENDDOCUMENT();
```

## Notes

- The first list passed to `DraggableProof` is the correct order.
- The second list holds items that should start in the target area (usually
  empty).
- Include `MathObjects.pl`; it is required by the macro.
- For partial credit on near-miss ordering, enable `Levenshtein` or
  `DamerauLevenshtein` scoring.
- Avoid HTML tables; use plain text or simple HTML spans for item labels.

## Testing

Render the problem with the local renderer before sharing:

```bash
source ./source_me.sh
pg-render -r -i path/to/problem.pgml
```

# Pedigree layout and rendering

This page owns native geometry, readability checks, and output scaling. Candidate ordering uses the
native-space measures defined here; see [PEDIGREE_RANKING.md](PEDIGREE_RANKING.md).

## Layout construction

[layout.py](pedigree_lib/layout.py) derives generations and partner blocks from fixed relationships,
then solves horizontal positions jointly with SciPy linear programming. It minimizes total row and
marriage spans subject to symbol/label clearances and centers each couple over its outermost
children. A sole child sits under the marriage midpoint; two children sit equally far to either
side. Larger sibships may use unequal gaps to accommodate spouses and descendant branches. Related
partner order and sibling order remain fixed, so the result is not an optimum over every possible
ordering.

Marrying-in spouses begin outside their sibling group. Layout tries reversing each such couple and
keeps collision-free reversals that reduce component width or reduce row and marriage spans at the
same width. It repeats until no reversal improves those dimensions. Positions are rounded to eight
decimal places to remove solver noise. Labels participate in clearance calculations. An infeasible
ordering or ambiguous geometry raises an explicit error for author revision.

Generation spacing leaves full-size symbols, short child drops, and room for labels. Separate
components have extra separation. Cousin unions receive double marriage lines; shared descendants
are drawn once. Mirroring changes geometry only, not relationships or labels. Some complex graphs
cannot be drawn without crossings by this compact layered method and are rejected. Authored ordering
hints can help without storing coordinates.

## Geometry acceptance

`layout_errors` rejects symbol or label collisions, lines through symbols or labels, and
intersections between unrelated relationship connectors. Both output renderers check the supplied
layout; neither renderer calculates it. One- and two-child alignment is checked against a tolerance
of 0.000001 native pixels for solver noise.

Aesthetics and ranking use native geometry before responsive display scaling. The largest
bottom-anchored empty rectangle fraction, `E`, divides its area by the tight bounding box of symbol
and connector strokes; canvas padding is excluded. Symbols and connector strokes both block empty
space, so connector bounds can affect the result. For `E`, the baseline is the bottom edge of the
lowest-generation symbol row. The obstacle boxes include symbol extents of 15 native units plus
half the non-scaling stroke (`1 / DISPLAY_SCALE`), and connector extents plus the same half-stroke.
Labels, canvas padding, and the HTML frame do not enter the measurement. The denominator is the
full tight symbol-and-connector bounding-box area.

`mean_row_density` is the average, excluding generation I, of `N_i / (max(x_i) - min(x_i) + 30)`
over each person row. The implementations are in
[geometry_features.py](pedigree_lib/geometry_features.py).

Affected-region fill uses person symbols only. The sibling pitch is `2 * RADIUS + SIBLING_GAP` =
58 native units, so each horizontal cell is four pitches (232 units) wide. Its left anchor is the
left edge of the leftmost symbol (`min(x) - RADIUS`). A person's cell is
`(generation_rank // 2, floor((x - left_anchor) / 232))`. The measure is the number of person-
occupied cells containing at least one visibly affected person divided by all person-occupied
cells, including generation I. Connector-only cells do not count. Implementation:
[affected_features.py](pedigree_lib/affected_features.py). Favorable ranking directions are in
[PEDIGREE_RANKING.md](PEDIGREE_RANKING.md).

## HTML and SVG output

HTML uses a positioned drawing table. Its width uses em units relative to question text and preserves
75% of native size at a 16 px font, growing with larger text. A keyboard-focusable horizontal scroll
region keeps wide drawings available without shrinking symbols. SVG exports preserve editable shapes
and text at 75% native size. Symbol outlines, connectors, and the HTML frame retain fixed 2 px
(1.5 pt) thickness; SVG uses `non-scaling-stroke`. HTML scales lengths and positions separately from
stroke thickness. This remains above 1 pt when browsers round CSS borders to whole pixels.

The drawing table has a class so Material does not wrap it in an article-table scrolling container.
The shared QTI self-test gives rich matching prompts the available column width; wider drawings
scroll locally. No remote site publication is part of the homework generation workflow.

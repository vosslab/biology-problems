# How to Make Graphs in WebWork PG/PGML

This guide covers creating graphs in PG/PGML problems using the local PG 2.17 renderer. It focuses on `PGgraphmacros.pl` for static display graphs, which is the recommended approach when the graph is informational (not an answer mechanism).

---

## Quick Decision: Which Graph Macro?

| Need | Macro | Notes |
|------|-------|-------|
| Display-only graph (titration curve, data plot) | `PGgraphmacros.pl` | GD bitmap image, no answer entry |
| Student clicks/draws on graph | `parserGraphTool.pl` | JS canvas, registers answer entry |

**Rule of thumb:** If students answer via RadioButtons or other PGML widgets (not by clicking the graph), use `PGgraphmacros.pl`. GraphTool's `ans_rule()` creates a phantom answer entry that can interfere with subsequent PGML answer evaluators.

---

## PGgraphmacros: Static Display Graphs

### Minimal Example

```perl
loadMacros(
  'PGstandard.pl',
  'MathObjects.pl',
  'PGML.pl',
  'PGgraphmacros.pl',
  'PGcourse.pl',
);

# Create graph: init_graph(xmin, ymin, xmax, ymax, ...)
$gr = init_graph(-1, 0, 10, 14,
  axes  => [0, 0],
  grid  => [11, 14],
  size  => [480, 400],
);

# Plot a function (string formula, not a code reference)
add_functions($gr,
  "2 + 3*sin(x) for x in <0,10> using color:blue and weight:2"
);

# Render as an image
$graph_img = image(insertGraph($gr), width => 480, height => 400, tex_size => 700);

BEGIN_PGML
Here is a graph:

[$graph_img]*
END_PGML
```

Key points:
- `init_graph` returns a GD graph object.
- `add_functions` takes a **string** formula with `for x in <min,max> using color:COLOR and weight:N`.
- `image(insertGraph($gr), ...)` produces an `<img>` HTML tag.
- Use `[$graph_img]*` in PGML (the `*` prevents HTML escaping).

### init_graph Parameters

```perl
$gr = init_graph($xmin, $ymin, $xmax, $ymax,
  axes  => [$x_origin, $y_origin],  # where axes cross
  grid  => [$x_divisions, $y_divisions],  # grid line count
  size  => [$width_px, $height_px],  # image dimensions
);
```

- `axes => [0, 0]` places the origin at (0, 0).
- `grid` controls the number of light grid lines (not tick labels).
- `size` sets the GD image dimensions in pixels.

### Adding Labels

```perl
# Axis labels at edges of plot area
$gr->lb(new Label($xmax, $ymin - 0.7, 'x-axis label', 'black', 'right', 'top'));
$gr->lb(new Label($xmin - 0.1, $ymax, 'y-axis', 'black', 'right', 'top'));

# Tick labels on y-axis
for $yv (0, 2, 4, 6, 8, 10, 12) {
  $gr->lb(new Label($xmin - 0.08, $yv, $yv, 'black', 'right', 'middle'));
}

# Tick labels on x-axis
for $xv (0, 1, 2, 3) {
  $gr->lb(new Label($xv, $ymin - 0.3, $xv, 'black', 'center', 'top'));
}
```

Label constructor: `new Label($x, $y, $text, $color, $h_align, $v_align)`

- `$h_align`: `'left'`, `'center'`, `'right'`
- `$v_align`: `'top'`, `'middle'`, `'bottom'`
- Labels are positioned in graph coordinates (not pixel coordinates).

### add_functions Syntax

The function string format:

```
"FORMULA for x in <XMIN,XMAX> using color:COLOR and weight:WEIGHT"
```

- `FORMULA`: A Perl math expression using `x` as the variable (e.g., `2*x**3 + x - 1`).
- `<XMIN,XMAX>`: Domain interval (angle brackets).
- `color:COLOR`: `blue`, `red`, `green`, `black`, etc.
- `weight:WEIGHT`: Line thickness in pixels (1, 2, 3, ...).

For computed coefficients, interpolate into the string:

```perl
$a = 0.5;
$b = -1.2;
$c = 3.0;
$d = 1.5;
$func_str = "$a*x**3 + $b*x**2 + $c*x + $d";
add_functions($gr, "$func_str for x in <0,3> using color:blue and weight:2");
```

### Multiple Curves

```perl
add_functions($gr,
  "$curve1 for x in <0,10> using color:blue and weight:2",
  "$curve2 for x in <0,10> using color:red and weight:2",
);
```

### Point-by-Point Curves with moveTo/lineTo

When a formula string cannot express the curve shape (e.g., parametric curves, physical models where x is not the independent variable), draw point-by-point:

```perl
$first_pt = 1;
for $i (0..400) {
  $t = $i / 400.0;
  # compute ($x_val, $y_val) from $t
  if ($first_pt) {
    $gr->moveTo($x_val, $y_val);
    $first_pt = 0;
  } else {
    $gr->lineTo($x_val, $y_val, 'blue', 2);
  }
}
```

This approach is essential for curves where the x-axis value is a computed function of the sweep variable rather than the independent variable itself. Use 300-400 points for smooth results.

### Dashed Lines

PGgraphmacros has no built-in dash style. Draw dashes manually as short line segments with gaps:

```perl
# Horizontal dashed line at y=$pka from x=0 to x=$xeq
for $d (0..29) {
  $x1d = $d * 0.10;
  $x2d = $x1d + 0.05;
  if ($x1d < $xeq) {
    if ($x2d > $xeq) { $x2d = $xeq; }
    $gr->moveTo($x1d, $pka);
    $gr->lineTo($x2d, $pka, 'gray', 1);
  }
}
```

Tune dash length (0.05) and gap (0.05) relative to graph coordinates. For vertical dashes, swap x/y in the loop.

### Dots and Stamps

```perl
# Filled circle at a point
$gr->stamps(closed_circle($x, $y, 'black'));

# Open circle
$gr->stamps(open_circle($x, $y, 'black'));
```

---

## Label Sizing: Why Labels Look Small and How to Fix It

**Labels in PGgraphmacros are GD bitmap text.** This has important consequences:

- `tex_size` on `image()` only affects TeX/PDF output, not HTML/GD output.
- TeX size commands (`\Large`, `\huge`) in label strings render as literal text in GD, not as formatting.
- `GD::Font->Giant` is accessible in the safe compartment (`$lb->font(GD::Font->Giant)`) but the largest GD bitmap font (9x15px) is still small.
- **Rendering at 2x and displaying at 1x makes labels half-size.** GD text is fixed-pixel; there is no "display DPI" concept.

### Pragmatic Approach for Readable Labels

Keep `size` at the final display dimensions (no 2x trick). Improve readability through layout:

```perl
# Slightly larger canvas
$gr = init_graph(-0.6, -1.2, 3.4, 12.5,
  axes => [0, 0],
  grid => [8, 5],
  size => [520, 420],
);

# Axis labels at edges (right-aligned at plot boundary)
$gr->lb(new Label(3.4, -0.7, 'OH- (equivalents)', 'black', 'right', 'top'));
$gr->lb(new Label(-0.1, 12.5, 'pH', 'black', 'right', 'top'));

# Fewer tick labels to reduce crowding
for $yv (0, 2, 4, 6, 8, 10, 12) {
  $gr->lb(new Label(-0.08, $yv, $yv, 'black', 'right', 'middle'));
}

$graph_img = image(insertGraph($gr), width => 520, height => 420, tex_size => 700);
```

Key techniques:
- **Widen graph bounds** beyond data range (`-0.6` to `3.4` instead of `0` to `3`) to create margin space for labels.
- **Place axis labels at edges** using `$xmax`/`$ymax` coordinates with `'right', 'top'` alignment.
- **Reduce tick label count** to avoid crowding (every 2 or 4 units instead of every 1).
- **Use high contrast** (black text on white background).

### GD Font Sizes (for reference)

Available via `$label->font(GD::Font->NAME)`:

| Font | Pixel Size | Notes |
|------|-----------|-------|
| `Tiny` | 5x8 | Too small for most uses |
| `Small` | 6x12 | Default in most PG builds |
| `MediumBold` | 7x13 | Slightly larger |
| `Large` | 8x16 | |
| `Giant` | 9x15 | Largest available |

All are fixed-size bitmap fonts. The size difference between Small and Giant is modest.

---

## Worked Example: Triprotic Titration Curve

A single cubic polynomial **cannot** produce the correct titration curve shape for a molecule with three pKa values. A cubic has at most one inflection point, but a 3-pKa titration needs three sigmoid steps.

### Physical Speciation Model (Correct Shape)

Sweep pH and compute the equivalents of base (n_bar) from the charge balance:

```
n_bar = (Ka1*H^2 + 2*Ka1*Ka2*H + 3*Ka1*Ka2*Ka3)
      / (H^3 + Ka1*H^2 + Ka1*Ka2*H + Ka1*Ka2*Ka3)
```

This gives the exact titration curve: three sigmoid steps with buffer flats at half-equivalence points (0.5, 1.5, 2.5 eq) and steep transitions at equivalence points (1.0, 2.0 eq).

```perl
$Ka1_val = 10**(-$pKa1_num);
$Ka2_val = 10**(-$pKaR_num);
$Ka3_val = 10**(-$pKa2_num);

$num_pts = 400;
$ph_lo = 0.5;
$ph_hi = 12.5;
$first_pt = 1;
for $i (0..$num_pts) {
  $ph_sweep = $ph_lo + ($ph_hi - $ph_lo) * $i / $num_pts;
  $H_conc = 10**(-$ph_sweep);

  $denom = $H_conc**3
         + $Ka1_val * $H_conc**2
         + $Ka1_val * $Ka2_val * $H_conc
         + $Ka1_val * $Ka2_val * $Ka3_val;
  $nbar = ($Ka1_val * $H_conc**2
         + 2 * $Ka1_val * $Ka2_val * $H_conc
         + 3 * $Ka1_val * $Ka2_val * $Ka3_val) / $denom;

  if ($nbar >= 0 && $nbar <= 3.0) {
    if ($first_pt) {
      $gr->moveTo($nbar, $ph_sweep);
      $first_pt = 0;
    } else {
      $gr->lineTo($nbar, $ph_sweep, 'blue', 2);
    }
  }
}
```

Note: this sweeps pH (y-axis) uniformly and computes equivalents (x-axis) as the dependent variable. The `moveTo`/`lineTo` approach handles this naturally since x is not the sweep variable.

### Why Not a Cubic?

A cubic `ax^3 + bx^2 + cx + d` through four points (e.g., (0, 1.5), (1, pKa1), (2, pKaR), (3, 12)):
- Has only **one inflection point** -- a triprotic titration needs three sigmoid transitions.
- Anchors pKa values at integer equivalents (1, 2) instead of the correct half-equivalents (0.5, 1.5, 2.5).
- Produces a smooth bend, not the characteristic "staircase with shoulders" shape.

### Alternative: Stacked Logistic Sigmoids

If you do not need physical accuracy, three logistic functions centered at half-equivalents approximate the shape:

```perl
$k = 10;  # steepness
$y0 = 1.0;
$y_top = 11.5;

for $i (0..300) {
  $xx = 3.0 * $i / 300.0;
  $s1 = 1 / (1 + exp(-$k * ($xx - 0.5)));
  $s2 = 1 / (1 + exp(-$k * ($xx - 1.5)));
  $s3 = 1 / (1 + exp(-$k * ($xx - 2.5)));

  $ph = $y0
      + ($pKa1_num - $y0) * $s1
      + ($pKaR_num - $pKa1_num) * $s2
      + ($pKa2_num - $pKaR_num) * $s3
      + ($y_top - $pKa2_num) * $s3 * 0.20;

  # draw with moveTo/lineTo as above
}
```

Note: the stacked-logistic curve does **not** pass exactly through pKa at each half-equivalence point. The speciation model is preferred for accuracy.

---

## GraphTool: Interactive Graphs (Use with Caution)

`parserGraphTool.pl` creates a JS-based interactive canvas where students can draw or place points.

### Known Issue: Answer Evaluator Interference

GraphTool's `ans_rule()` registers an answer entry (typically `AnSwEr0001`). This shifts the numbering of subsequent PGML answer blanks and can cause `"Unrecognized evaluator type ||"` errors on later RadioButtons or other PGML widgets.

**Workaround:** If you must use GraphTool alongside PGML answers:
- Place GraphTool in a `BEGIN_TEXT` block with `\{$gt->ans_rule()\}`.
- Use `LABELED_ANS($gt_ans_id, $gt_checker)` before the PGML block.
- Keep RadioButtons and other widgets in a separate `BEGIN_PGML` block.

**Better approach:** If the graph is display-only, use `PGgraphmacros.pl` instead.

### GraphTool Minimal Pattern (for reference)

```perl
loadMacros('parserGraphTool.pl');

$gt = GraphTool()->with(
  bBox        => [-1, 14, 14, -1],
  gridX       => 1,
  gridY       => 1,
  xAxisLabel  => 'x',
  yAxisLabel  => 'y',
  availableTools  => ['PointTool'],
  staticObjects   => ['{cubic,solid,(0,2),(4,3.8),(7,4.6),(12,12)}'],
);

BEGIN_TEXT
\{$gt->ans_rule()\}
END_TEXT

$gt_checker = AnswerEvaluator->new;
$gt_checker->install_evaluator(sub { ... });
LABELED_ANS($gt->ANS_NAME, $gt_checker);
```

---

## Variable Scoping Reminder

Do **not** use `my` on any variable that PGML needs to interpolate. PG runs in a safe compartment where `my` variables are invisible to PGML.

```perl
# WRONG - invisible to PGML
my $graph_img = image(insertGraph($gr), ...);

# RIGHT - package-level, visible to PGML
$graph_img = image(insertGraph($gr), ...);
```

See [PG_COMMON_PITFALLS.md](PG_COMMON_PITFALLS.md) for more scoping details.

---

## Sizing and Margins

The `size` parameter in `init_graph` sets the GD image pixel dimensions. The `width` and `height` in `image()` control the HTML display size. **Always keep these matched at 1x** -- rendering at 2x and displaying at 1x shrinks bitmap labels.

```perl
# Good: matched sizes, extra margin from wider bounds
$gr = init_graph(-0.6, -1.2, 3.4, 12.5,
  axes => [0, 0],
  grid => [8, 5],
  size => [520, 420],
);
$graph_img = image(insertGraph($gr), width => 520, height => 420, tex_size => 700);
```

To create margin space for labels without shrinking the data region, widen the graph bounds beyond the data range (e.g., `-0.6` to `3.4` for data spanning 0 to 3).

`tex_size` controls the image width in TeX/PDF output only (700 = 70% of text width). It has no effect on HTML/GD rendering.

---

## Macros Not Available in This Renderer

The following graph-related macros exist in the OPL but are **not** available in the local PG 2.17 renderer:

- `PGlateximage.pl` (LaTeX-to-image pipeline, requires LaTeX installation)
- `PGtikz.pl` (TikZ/pgfplots, requires LaTeX installation)

Stick to `PGgraphmacros.pl` for display graphs and `parserGraphTool.pl` for interactive graphs.

---

## Related Documentation

- [PG_2_17_RENDERER_MACROS.md](PG_2_17_RENDERER_MACROS.md) - Full list of available macros
- [PG_COMMON_PITFALLS.md](PG_COMMON_PITFALLS.md) - Variable scoping, PGML parsing issues
- [WEBWORK_PROBLEM_AUTHOR_GUIDE.md](WEBWORK_PROBLEM_AUTHOR_GUIDE.md) - Overall problem structure

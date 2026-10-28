# Preferred slide colors

The instructor's preferred emphasis palette is independent of LibreOffice's named colors.
Use explicit hex values in Djot, for example `[Predict]{color=#D40000}`.
Preserve meaningful color relationships in the original slides; match references to the
items they identify. Course theme colors and pale background fills serve separate roles.

## Standard text palette

These values come from the HTML span styles in `replacement_rules` in
`~/nsh/PROBLEMS/biology-problems/problems/matching_sets/TEMPLATE.yml`.
Names below preserve that source's labels.

| Color | Hex |
| --- | --- |
| Red | `#D40000` |
| Dark orange | `#B74300` |
| Light orange | `#935D00` |
| Dark yellow | `#6C6C00` |
| Lime green | `#3B7600` |
| Green | `#007A00` |
| Teal | `#00775F` |
| Cyan | `#007576` |
| Sky blue | `#076DAD` |
| Blue | `#003FFF` |
| Navy | `#0067CC` |
| Purple | `#A719DB` |
| Magenta | `#C80085` |
| Pink | `#CC0066` |

## Procedure sequences

Use well-separated colors from the fixed palette in rainbow order for new colored step sequences.
For six steps, use Red, Dark orange, Dark yellow, Green, Blue, Purple. For four steps, use Red,
Green, Blue, Purple. Keep each repeated roadmap identical and match step cross-references to its
own method's colors. Preserve meaningful source colors when converting existing material unless
recoloring is requested.

## Three-point testcross pairs

Reserve green for the two original parental rows and lime green for other offspring with a
parental combination for the selected gene pair. Color each pair's recombinant rows, summary
label/results, and final percentage consistently. The fixed base colors identify the pair;
lighter fills keep dark table text readable. Keep each role's hue and HSL saturation stable;
vary lightness between text/line colors and fills. Pair labels also use the base text color
so a pale background and a saturated map line have a direct visual connection.

| Meaning | Fixed palette base | Table fill |
| --- | --- | --- |
| Original parental rows | Green `#007A00` | `#8FFF8F` |
| Other pairwise parental rows | Lime green `#3B7600` | `#D6FFAD` |
| CD recombinants/results | Red `#D40000` | `#FF8F8F` |
| CH recombinants/results | Blue `#003FFF` | `#8FABFF` |
| DH recombinants/results | Purple `#A719DB` | `#DC9AF4` |

These fills use 78% HSL lightness, except lime at 84% to distinguish it from the original
parents. Saturation matches the base (100% except purple at approximately 79.5%), within
8-bit RGB rounding. Repeat these same fills in the allele-comparison diagrams and tables.

Retain gray on the covered gene column, including its intersection with colored rows.
Unknown classifications/results stay unrevealed. The six-step roadmap retains its own established
step colors; pair colors track the data through the calculation and summary tables.

## Instructor's color-wheel tool

For additional color sets, use the instructor-developed tool at
`~/nsh/PROBLEMS/qti-package-maker/qti_package_maker/common/color_wheel.py`.
Its public `generate_color_wheel(num_colors, backend="cam16", **kwargs)` API generates
perceptually distinct colors. CAM16 is the default backend; `legacy` is also available.
The module exposes named `dark_color_wheel`, `light_color_wheel`, and
`extra_light_color_wheel` dictionaries generated with modes `dark`, `light`, and `xlight`.

Returned hex strings omit the leading `#`; add it when authoring Djot color attributes.
Generated wheels are an option for additional palettes, not an exact reproduction of the
fixed template palette above. Keep chosen values explicit in slide sources so rebuilding a
deck does not depend on a sibling checkout or silently change its colors.

Choose text and background colors for their actual role and check the rendered result.
Perceptual separation does not by itself guarantee readable text contrast.
See [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md) for the instructor's presentation requirements.

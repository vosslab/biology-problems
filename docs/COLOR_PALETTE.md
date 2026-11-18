# Shared color palette

> This file is vendored. Local changes can and will be overwritten by propagation.

Use the 91 colors below as the source colors for authored diagrams, charts, illustrations,
slides, question visuals, and visualizations within applications. The published hex values
define the palette.

## Hue families

Use Dark for colored text on light surfaces, Light or Pastel for fills under dark labels, and
Medium for colored marks. Choose Extra light for pale backgrounds and Extra dark for deep
accents. Check each combination in its actual setting.

| Hue family | Extra light | Light | Medium | Dark | Extra dark | Pastel |
| --- | --- | --- | --- | --- | --- | --- |
| Red | `#FFCCCC` | `#FF8080` | `#FF1A1A` | `#D40000` | `#660000` | `#E3BFBF` |
| Dark orange | `#FFDFCC` | `#FFAE80` | `#FF6E1A` | `#B74300` | `#662500` | `#E3CCBF` |
| Light orange | `#FFECCC` | `#FFD080` | `#FFAB1A` | `#935D00` | `#603C00` | `#E3D6BF` |
| Dark yellow | `#FFFFCC` | `#FFFF80` | `#FFFF1A` | `#6C6C00` | `#464600` | `#E3E3BF` |
| Lime green | `#E6FFCC` | `#BFFF80` | `#8CFF1A` | `#3B7600` | `#264D00` | `#D1E3BF` |
| Green | `#CCFFCC` | `#80FF80` | `#1AFF1A` | `#007A00` | `#004F00` | `#BFE3BF` |
| Teal | `#CCFFF5` | `#80FFE5` | `#1AFFD1` | `#00775F` | `#004D3E` | `#BFE3DC` |
| Cyan | `#CCFFFF` | `#80FEFF` | `#1AFDFF` | `#007576` | `#004C4D` | `#BFE3E3` |
| Sky blue | `#CEEBFD` | `#84CDFA` | `#22A4F6` | `#076DAD` | `#043E62` | `#C0D5E2` |
| Blue | `#CCD9FF` | `#809FFF` | `#1A52FF` | `#003FFF` | `#001966` | `#BFC8E3` |
| Navy | `#CCE6FF` | `#80C0FF` | `#1A8DFF` | `#0067CC` | `#003366` | `#BFD1E3` |
| Purple | `#EFD1FA` | `#D78DF2` | `#B731E7` | `#A719DB` | `#460A5C` | `#D8C3E0` |
| Magenta | `#FFCCEE` | `#FF80D4` | `#FF1AB2` | `#C80085` | `#660044` | `#E3BFD7` |
| Pink | `#FFCCE6` | `#FF80BF` | `#FF1A8C` | `#CC0066` | `#660033` | `#E3BFD1` |

The Dark column preserves the original text accents. The other grades keep each Dark color's
HSL hue and saturation, with lightness set to 90%, 75%, and 55% for Extra light, Light, and
Medium. Extra dark uses the smaller of 20% lightness and 65% of the Dark color's lightness.
Pastel keeps the hue, sets lightness to 82%, and uses 40% of the original saturation. The
table records the resulting rounded sRGB values for direct use.

## Neutrals

Use neutrals for ordinary text, outlines, axes, gridlines, backgrounds, or subdued details.

| Neutral | Hex |
| --- | --- |
| Black | `#000000` |
| Charcoal | `#333333` |
| Dark gray | `#666666` |
| Gray | `#999999` |
| Light gray | `#CCCCCC` |
| Extra light gray | `#EEEEEE` |
| White | `#FFFFFF` |

## Use colors together

Combine palette colors freely through gradients, transparency, layering, and blending. The
intermediate colors are rendering results. Choose the source colors for these effects from
the tables above. For a tinted background, try an Extra light shade, a Pastel, or a palette
color layered over a neutral surface.

- Use Blue Dark for a label on white and Blue Pastel to echo its hue behind black text.
- Use Blue Dark and Light orange Dark for two chart series, with distinct markers and labels.
- Use a White-to-Teal Extra light gradient behind a Charcoal caption.

Assess contrast and distinguishability for the intended use, background, and audience. Check
text against the surface it actually appears on, including the result of any layering.
See [COLOR_CONTRAST_ACCESSIBILITY.md](COLOR_CONTRAST_ACCESSIBILITY.md).

## Record local assignments

The shared palette governs color selection. Repository-specific guidance assigns approved
colors to concepts and roles. Record recurring assignments in `docs/REPO_COLOR_PALETTE.md`
with the palette family, the shade used for each purpose, and the material where the
assignment applies. Reuse the assignment across related figures, legends, labels, tables,
and references.
When color distinguishes categories, use distinct families and identify them with labels, shapes,
or patterns as well as color.

The QTI Package Maker (QPM) color wheel can help explore hue spacing. Select the final colors
from the tables above.

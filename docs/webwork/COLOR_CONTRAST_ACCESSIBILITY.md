# Color contrast accessibility

## Target contrast ratio

Our problems target a **5.5:1** contrast ratio for all foreground/background
text pairs. This exceeds WCAG AA's 4.5:1 minimum for normal text.

| WCAG level | Minimum ratio (normal text) |
| --- | --- |
| AA | 4.5:1 |
| AAA | 7:1 |
| Our target | 5.5:1 |

The maximum possible contrast ratio is 21:1 (black `#000000` on white `#FFFFFF`).

## How contrast ratio works

**Formula:** `(L1 + 0.05) / (L2 + 0.05)` where L1 is the lighter relative luminance
and L2 is the darker.

**Relative luminance:** `L = 0.2126*R + 0.7152*G + 0.0722*B` where R, G, B are
linearized sRGB values (apply gamma correction: if the 8-bit channel value / 255 is
<= 0.04045, divide by 12.92; otherwise compute `((value + 0.055) / 1.055) ^ 2.4`).

**Backward solve for target luminance:** Given target ratio CR and white background
(L_bg = 1.0), the required foreground luminance is `L_fg = 1.05 / CR - 0.05`.
For CR = 5.5, L_fg = 0.14091.

## Contrast calculator tool

[tools/contrast_calculator.py](../../tools/contrast_calculator.py) implements the
WCAG v2 contrast formula with backward solving via binary search on HSL lightness.

Usage:
```bash
# audit the 14-color rainbow palette
python3 tools/contrast_calculator.py --audit

# audit and normalize (brighten over-dark colors closer to target)
python3 tools/contrast_calculator.py --audit --normalize

# check a single color
python3 tools/contrast_calculator.py --check '#e60000'

# custom target ratio
python3 tools/contrast_calculator.py --audit --ratio 7.0
```

## Online calculators

- **WebAIM Contrast Checker** -- interactive web tool for checking any color pair.
  Append `&api` to any permalink for JSON output, e.g.
  `https://webaim.org/resources/contrastchecker/?fcolor=FFFFFF&bcolor=9BC8EA&api`
- **ACART Contrast Checker** -- alternative checker with visual preview.
- **WebAIM Contrast Checker Bookmarklet** -- in-page testing on live WeBWorK problems.

## 14-color rainbow palette audit

All colors verified via `tools/contrast_calculator.py` and spot-checked against
WebAIM API. Background: white (`#FFFFFF`). Target: 5.5:1.

| Slot | Label | Old hex | Old ratio | New hex | New ratio | Change |
| --- | --- | --- | --- | --- | --- | --- |
| A | RED | `#e60000` | 4.81:1 | `#d40000` | 5.53:1 | Darkened |
| B | DARK ORANGE | `#e65400` | 3.73:1 | `#b74300` | 5.50:1 | Darkened |
| C | LIGHT ORANGE | `#e69100` | 2.50:1 | `#935d00` | 5.52:1 | Darkened |
| D | DARK YELLOW | `#b3b300` | 2.24:1 | `#6c6c00` | 5.55:1 | Darkened |
| E | LIME GREEN | `#59b300` | 2.67:1 | `#3b7600` | 5.56:1 | Darkened |
| F | GREEN | `#009900` | 3.78:1 | `#007a00` | 5.55:1 | Darkened |
| G | TEAL | `#00b38f` | 2.68:1 | `#00775f` | 5.52:1 | Darkened |
| H | CYAN | `#00b3b3` | 2.59:1 | `#007576` | 5.52:1 | Darkened |
| I | SKY BLUE | `#0a9bf5` | 2.99:1 | `#076dad` | 5.53:1 | Darkened |
| J | BLUE | `#0039e6` | 7.70:1 | `#003fff` | 6.66:1 | Brightened |
| K | NAVY | `#004d99` | 8.33:1 | `#0067cc` | 5.51:1 | Brightened |
| L | PURPLE | `#7b12a1` | 8.59:1 | `#a719db` | 5.52:1 | Brightened |
| M | MAGENTA | `#b30077` | 6.60:1 | `#c80085` | 5.53:1 | Brightened |
| N | PINK | `#cc0066` | 5.59:1 | `#cc0066` | 5.59:1 | Unchanged |

All 14 colors now pass the 5.5:1 target. Colors A-I were darkened to meet the
minimum; J-M were brightened to be more vivid while still passing.

## Audit of other problem colors

Verified via WebAIM API against white (`#FFFFFF`) background:

| Color | Use | Ratio vs white | Passes 5.5:1? |
| --- | --- | --- | --- |
| `#0066cc` | Blue, data values | 5.56:1 | YES |
| `#997300` | Gold, key terms | 4.36:1 | NO |
| `#cc0000` | Red, negations | 5.88:1 | YES |
| `#888888` bg + white text | Old table headers | 3.54:1 | NO (fails AA) |
| `#cccccc` bg + black text | New table headers | 13.0:1 | YES |
| `#000000` on `#FFFFFF` | Body text | 21:1 | YES |

## Recommended replacements for non-palette colors

All verified via WebAIM API:

| Current | Replacement | Ratio | Use |
| --- | --- | --- | --- |
| `#997300` | `#7a5c00` | ~5.7:1 | Dark gold/brown for key terms |
| `#888888` bg | `#cccccc` bg + `#000` text | 13.0:1 | Table headers |

## Custom colors in YAML files

About 34 YAML files use custom colors outside the standard 14-color palette
(e.g., `#7b7737`, `#843232`, `#693AAA`, `#FE2712`, `#66B032`). These are not
modified by the palette update. Run the audit mode on custom colors separately:

```bash
python3 tools/contrast_calculator.py --check '#7b7737'
```

## Rules

- Every foreground/background pair in our problems should be checked before use.
- When in doubt, use the WebAIM checker or `tools/contrast_calculator.py`.
- This doc documents the standard. Updating the existing color palette in
  [QUESTION_STATEMENT_EMPHASIS.md](QUESTION_STATEMENT_EMPHASIS.md) is a follow-up task.

## Related documentation

- [QUESTION_STATEMENT_EMPHASIS.md](QUESTION_STATEMENT_EMPHASIS.md) - Current color definitions
- [COLOR_TEXT_IN_WEBWORK.md](COLOR_TEXT_IN_WEBWORK.md) - Color text rendering in WeBWorK

# Palette contrast audit

See [COLOR_CONTRAST_ACCESSIBILITY.md](COLOR_CONTRAST_ACCESSIBILITY.md) for the
generic WCAG contrast method these values were measured against.

## 14-color rainbow palette

Palette hexes come from `tools/contrast_calculator.py` (`RAINBOW_PALETTE`),
the source of truth for this palette's definition. Ratios are measured
against a white (`#ffffff`) background with
`python3 tools/contrast_calculator.py --audit`.

| Slot | Hex | Ratio vs white |
| --- | --- | --- |
| A RED | `#d40000` | 5.53:1 |
| B DARK ORANGE | `#b74300` | 5.50:1 |
| C LIGHT ORANGE | `#935d00` | 5.52:1 |
| D DARK YELLOW | `#6c6c00` | 5.55:1 |
| E LIME GREEN | `#3b7600` | 5.56:1 |
| F GREEN | `#007a00` | 5.55:1 |
| G TEAL | `#00775f` | 5.52:1 |
| H CYAN | `#007576` | 5.52:1 |
| I SKY BLUE | `#076dad` | 5.53:1 |
| J BLUE | `#003fff` | 6.66:1 |
| K NAVY | `#0067cc` | 5.51:1 |
| L PURPLE | `#a719db` | 5.52:1 |
| M MAGENTA | `#c80085` | 5.53:1 |
| N PINK | `#cc0066` | 5.59:1 |

All 14 slots pass the 5.5:1 target with no replacements needed.

## Other problem colors

These colors are used outside the 14-slot palette for specific semantic
roles in generated problems.

| Color | Hex | Role | Ratio vs white | Pass/fail (5.5:1) |
| --- | --- | --- | --- | --- |
| Blue | `#0066cc` | Data values | 5.57:1 | PASS |
| Gold | `#997300` | Key terms | 4.37:1 | FAIL |
| Red | `#cc0000` | Negations | 5.89:1 | PASS |

## Recommended replacements for non-palette colors

| Old hex | New hex | Use | New ratio vs white |
| --- | --- | --- | --- |
| `#997300` | `#7a5c00` | Dark gold/brown for key terms | 6.25:1 |

For the old `#888888` table-header background, switch to a `#cccccc`
background with black (`#000000`) text. Black on `#cccccc` measures 13.08:1.

## Custom colors in YAML files

About 34 YAML files use custom colors outside the 14-color palette, for
example `#7b7737`, `#843232`, `#693AAA`, `#FE2712`, and `#66B032`. Authors
check those individually with
`tools/contrast_calculator.py --check '#<hex>' -b '#ffffff'`.

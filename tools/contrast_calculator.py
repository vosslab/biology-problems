#!/usr/bin/env python3
"""Compute WCAG v2 contrast ratios and find accessible color shades.

Backward-solves the WCAG contrast formula to find the brightest shade
of a given hue that meets a target contrast ratio against white.
"""

# Standard Library
import colorsys
import argparse

#============================================
def linearize_channel(value: int) -> float:
	"""Convert an 8-bit sRGB channel to linear RGB.

	Args:
		value: 8-bit channel value (0-255).

	Returns:
		Linear RGB value (0.0-1.0).
	"""
	# normalize to 0-1 range
	srgb = value / 255.0
	if srgb <= 0.04045:
		linear = srgb / 12.92
	else:
		linear = ((srgb + 0.055) / 1.055) ** 2.4
	return linear

#============================================
def relative_luminance(r: int, g: int, b: int) -> float:
	"""Compute WCAG relative luminance from 8-bit RGB values.

	Args:
		r: Red channel (0-255).
		g: Green channel (0-255).
		b: Blue channel (0-255).

	Returns:
		Relative luminance (0.0-1.0).
	"""
	r_lin = linearize_channel(r)
	g_lin = linearize_channel(g)
	b_lin = linearize_channel(b)
	luminance = 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin
	return luminance

#============================================
def hex_to_rgb(hex_color: str) -> tuple:
	"""Convert a hex color string to an (R, G, B) tuple.

	Args:
		hex_color: Color string like '#e60000' or 'e60000'.

	Returns:
		Tuple of (r, g, b) integers.
	"""
	hex_color = hex_color.lstrip('#')
	r = int(hex_color[0:2], 16)
	g = int(hex_color[2:4], 16)
	b = int(hex_color[4:6], 16)
	return (r, g, b)

#============================================
def rgb_to_hex(r: int, g: int, b: int) -> str:
	"""Convert RGB integers to a hex color string.

	Args:
		r: Red channel (0-255).
		g: Green channel (0-255).
		b: Blue channel (0-255).

	Returns:
		Hex color string like '#e60000'.
	"""
	hex_str = f"#{r:02x}{g:02x}{b:02x}"
	return hex_str

#============================================
def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
	"""Compute WCAG v2 contrast ratio between two colors.

	Args:
		fg_hex: Foreground color hex string.
		bg_hex: Background color hex string.

	Returns:
		Contrast ratio (1.0-21.0).
	"""
	fg_rgb = hex_to_rgb(fg_hex)
	bg_rgb = hex_to_rgb(bg_hex)
	l_fg = relative_luminance(*fg_rgb)
	l_bg = relative_luminance(*bg_rgb)
	# lighter luminance goes on top
	lighter = max(l_fg, l_bg)
	darker = min(l_fg, l_bg)
	ratio = (lighter + 0.05) / (darker + 0.05)
	return ratio

#============================================
def find_accessible_shade(hex_color: str, target_ratio: float,
		bg_hex: str = "#ffffff") -> str:
	"""Find the brightest shade of a hue meeting the target contrast ratio.

	Preserves hue and saturation from the original color. Uses binary
	search on HSL lightness to find the shade whose relative luminance
	yields exactly the target contrast ratio against the background.

	Args:
		hex_color: Original color hex string.
		target_ratio: Desired minimum contrast ratio.
		bg_hex: Background color hex string (default white).

	Returns:
		Hex color string of the accessible shade.
	"""
	# convert original to HSL to preserve hue and saturation
	r, g, b = hex_to_rgb(hex_color)
	# colorsys uses 0-1 range for RGB
	h, l_orig, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

	# compute the target foreground luminance for the given ratio
	# contrast_ratio = (L_bg + 0.05) / (L_fg + 0.05) when bg is lighter
	bg_rgb = hex_to_rgb(bg_hex)
	l_bg = relative_luminance(*bg_rgb)
	# target_fg_luminance from: ratio = (l_bg + 0.05) / (l_fg + 0.05)
	target_lum = (l_bg + 0.05) / target_ratio - 0.05

	# binary search on lightness (lower = darker = higher contrast)
	low = 0.0
	high = l_orig
	best_hex = hex_color

	for _i in range(64):
		mid = (low + high) / 2.0
		# convert HSL back to RGB
		r_f, g_f, b_f = colorsys.hls_to_rgb(h, mid, s)
		r_int = round(r_f * 255)
		g_int = round(g_f * 255)
		b_int = round(b_f * 255)
		# clamp to valid range
		r_int = max(0, min(255, r_int))
		g_int = max(0, min(255, g_int))
		b_int = max(0, min(255, b_int))
		# compute luminance of this candidate
		lum = relative_luminance(r_int, g_int, b_int)
		if lum > target_lum:
			# too bright, need darker
			high = mid
		else:
			# dark enough or too dark, try brighter
			low = mid
			best_hex = rgb_to_hex(r_int, g_int, b_int)

	# final refinement: use the midpoint result
	mid = (low + high) / 2.0
	r_f, g_f, b_f = colorsys.hls_to_rgb(h, mid, s)
	r_int = max(0, min(255, round(r_f * 255)))
	g_int = max(0, min(255, round(g_f * 255)))
	b_int = max(0, min(255, round(b_f * 255)))
	candidate = rgb_to_hex(r_int, g_int, b_int)
	# verify this candidate actually meets the ratio
	if contrast_ratio(candidate, bg_hex) >= target_ratio:
		best_hex = candidate

	return best_hex

#============================================
def find_brightest_accessible_shade(hex_color: str, target_ratio: float,
		bg_hex: str = "#ffffff") -> str:
	"""Find the brightest shade of a hue that just barely meets the target ratio.

	For colors that already exceed the target, this lightens them to be as
	vivid as possible while still meeting the minimum contrast requirement.

	Args:
		hex_color: Original color hex string.
		target_ratio: Desired minimum contrast ratio.
		bg_hex: Background color hex string (default white).

	Returns:
		Hex color string of the brightest accessible shade.
	"""
	# convert original to HSL to preserve hue and saturation
	r, g, b = hex_to_rgb(hex_color)
	h, l_orig, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

	# binary search: find the highest lightness that still meets the ratio
	# search between current lightness and 0.5 (max saturation point)
	low = l_orig
	high = 0.5
	best_hex = hex_color

	for _i in range(64):
		mid = (low + high) / 2.0
		r_f, g_f, b_f = colorsys.hls_to_rgb(h, mid, s)
		r_int = max(0, min(255, round(r_f * 255)))
		g_int = max(0, min(255, round(g_f * 255)))
		b_int = max(0, min(255, round(b_f * 255)))
		candidate = rgb_to_hex(r_int, g_int, b_int)
		ratio = contrast_ratio(candidate, bg_hex)
		if ratio >= target_ratio:
			# still passes, try brighter
			best_hex = candidate
			low = mid
		else:
			# too bright, go darker
			high = mid

	return best_hex

#============================================
def audit_palette(colors: dict, target_ratio: float,
		bg_hex: str = "#ffffff", normalize: bool = False) -> list:
	"""Audit a color palette and compute replacements for failing colors.

	Args:
		colors: Dict mapping label to hex color string.
		target_ratio: Target contrast ratio.
		bg_hex: Background color hex string.
		normalize: If True, also lighten passing colors to be closer to target.

	Returns:
		List of dicts with label, old_hex, new_hex, old_ratio, new_ratio, status.
	"""
	results = []
	for label, hex_color in colors.items():
		old_ratio = contrast_ratio(hex_color, bg_hex)
		passes = old_ratio >= target_ratio
		if not passes:
			# too light, darken to meet target
			new_hex = find_accessible_shade(hex_color, target_ratio, bg_hex)
			new_ratio = contrast_ratio(new_hex, bg_hex)
			status = "DARKENED"
		elif normalize and old_ratio > target_ratio + 0.5:
			# too dark, lighten to be closer to target (more vivid)
			new_hex = find_brightest_accessible_shade(
				hex_color, target_ratio, bg_hex
			)
			new_ratio = contrast_ratio(new_hex, bg_hex)
			if new_hex != hex_color:
				status = "BRIGHTENED"
			else:
				status = "PASS (unchanged)"
		else:
			new_hex = hex_color
			new_ratio = old_ratio
			status = "PASS (unchanged)"
		result = {
			"label": label,
			"old_hex": hex_color,
			"new_hex": new_hex,
			"old_ratio": old_ratio,
			"new_ratio": new_ratio,
			"status": status,
		}
		results.append(result)
	return results

#============================================
# the 14-color rainbow palette from replacement_rules
RAINBOW_PALETTE = {
	"A RED":          "#d40000",
	"B DARK ORANGE":  "#b74300",
	"C LIGHT ORANGE": "#935d00",
	"D DARK YELLOW":  "#6c6c00",
	"E LIME GREEN":   "#3b7600",
	"F GREEN":        "#007a00",
	"G TEAL":         "#00775f",
	"H CYAN":         "#007576",
	"I SKY BLUE":     "#076dad",
	"J BLUE":         "#003fff",
	"K NAVY":         "#0067cc",
	"L PURPLE":       "#a719db",
	"M MAGENTA":      "#c80085",
	"N PINK":         "#cc0066",
}

#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="WCAG v2 contrast ratio calculator and palette auditor"
	)
	mode_group = parser.add_mutually_exclusive_group()
	mode_group.add_argument(
		'-a', '--audit', dest='audit_mode', action='store_true',
		help='Audit the built-in 14-color rainbow palette'
	)
	mode_group.add_argument(
		'-c', '--check', dest='check_color', type=str,
		help='Check contrast ratio for a single hex color against white'
	)
	parser.add_argument(
		'-r', '--ratio', dest='target_ratio', type=float, default=5.5,
		help='Target contrast ratio (default: 5.5)'
	)
	parser.add_argument(
		'-b', '--background', dest='bg_hex', type=str, default='#ffffff',
		help='Background hex color (default: #ffffff)'
	)
	parser.add_argument(
		'-N', '--normalize', dest='normalize', action='store_true',
		help='Also lighten over-dark colors to be closer to the target ratio'
	)
	parser.set_defaults(normalize=False)
	args = parser.parse_args()
	return args

#============================================
def main():
	"""Main entry point."""
	args = parse_args()

	if args.check_color:
		# single color check mode
		hex_color = args.check_color
		ratio = contrast_ratio(hex_color, args.bg_hex)
		passes = ratio >= args.target_ratio
		status = "PASS" if passes else "FAIL"
		print(f"Color: {hex_color}")
		print(f"Background: {args.bg_hex}")
		print(f"Contrast ratio: {ratio:.2f}:1")
		print(f"Target: {args.target_ratio}:1 -> {status}")
		if not passes:
			new_hex = find_accessible_shade(
				hex_color, args.target_ratio, args.bg_hex
			)
			new_ratio = contrast_ratio(new_hex, args.bg_hex)
			print(f"Suggested replacement: {new_hex} ({new_ratio:.2f}:1)")
		return

	# default: audit mode for the built-in palette
	print(f"Auditing 14-color rainbow palette (target: {args.target_ratio}:1)")
	print(f"Background: {args.bg_hex}")
	print()

	results = audit_palette(
		RAINBOW_PALETTE, args.target_ratio, args.bg_hex, args.normalize
	)

	# print header
	header = f"{'Slot':<18} {'Old Hex':<10} {'Old Ratio':<12} {'New Hex':<10} {'New Ratio':<12} {'Status'}"
	print(header)
	print("-" * len(header))

	changed_count = 0
	for result in results:
		old_ratio_str = f"{result['old_ratio']:.2f}:1"
		new_ratio_str = f"{result['new_ratio']:.2f}:1"
		line = (
			f"{result['label']:<18} "
			f"{result['old_hex']:<10} "
			f"{old_ratio_str:<12} "
			f"{result['new_hex']:<10} "
			f"{new_ratio_str:<12} "
			f"{result['status']}"
		)
		print(line)
		if result['old_hex'] != result['new_hex']:
			changed_count += 1

	print()
	print(f"Colors updated: {changed_count}")
	print(f"Colors unchanged: {len(results) - changed_count}")

	# print sed-friendly replacement mapping
	print()
	print("Replacement mapping (old -> new):")
	for result in results:
		if result['old_hex'] != result['new_hex']:
			print(f"  {result['old_hex']} -> {result['new_hex']}")

#============================================
if __name__ == '__main__':
	main()

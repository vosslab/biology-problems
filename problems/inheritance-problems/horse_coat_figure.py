#!/usr/bin/env python3
"""Compose horse-coat figures from one chestnut drawing.

The OpenClipart chestnut paths are the anatomy. Coat artwork is authored by
hand and clipped to that body:

- base coat fills the body paths
- leopard spots are a library of irregular shapes, placed by eye
- frame patches are irregular white shapes that follow the shoulder, barrel, and hip
- the drawing's own socks stay on every coat so the lower legs remain readable
- mane, ears, muzzle, hooves, and the face are foreground details
- a stroke pass redraws the anatomical edges after the fills

The five coats are neither modeled pattern, frame-overo, leopard-complex,
fewspot, and Pintaloosa. Fewspot reuses the spot shapes but only a few of them,
on a white base.
"""

import math
import re
import shutil
import subprocess
from pathlib import Path

import shapely.geometry
import shapely.ops


CHESTNUT_SVG = Path(__file__).resolve().parents[2] / "chestnut_horse.svg"
FIGURE_SVG = Path(__file__).resolve().with_name("horse_coat_patterns.svg")
FIGURE_PNG = Path(__file__).resolve().with_name("horse_coat_patterns.png")

CHESTNUT = "#7b4014"
PALE = "#f3eee6"
WHITE = "#fcfbfa"
STRUCTURE = "#24180f"

# Original fill identifies the anatomical region. Coats do not invent regions.
REGION_BY_FILL = {
	"#7b4014": "coat",
	"#583b1d": "mane",
	"#2f1b03": "ear",
	"#fbf0e0": "muzzle",
	"#fcfbfa": "marking",
	"#ddc8c3": "hoof",
	"#0c0a00": "feature",
	"#0c0d00": "feature",
	"#494427": "feature",
}

DETAIL_FILL = {
	"mane": "#3d2918",
	"ear": "#2a1a0c",
	"muzzle": "#f0d2ae",
	"hoof": "#d7c0b0",
	"feature": "#14110e",
}

# The flank polygon is a geometric white. The small flank sliver draws a seam through patches.
GEOMETRIC_MARKING = "path1934"
FLANK_SLIVER = "path2866"

# Hand-drawn spot silhouettes, each centered near the origin.
SPOT_LIBRARY = {
	"blot": "M-18,-2 C-26,-16 -8,-24 2,-16 C14,-26 30,-10 22,2 C28,16 10,24 -2,16 C-18,22 -28,8 -18,-2 Z",
	"bean": "M-14,4 C-22,-8 -6,-18 6,-12 C16,-18 26,-4 16,8 C20,16 4,18 -6,12 C-18,16 -22,10 -14,4 Z",
	"comma": "M-2,-16 C10,-20 18,-8 12,0 C8,8 0,10 -4,4 C-12,12 -22,4 -16,-4 C-22,-14 -12,-18 -2,-16 Z",
	"peanut": "M-22,2 C-26,-10 -14,-14 -6,-8 C2,-16 14,-12 16,-4 C26,-6 26,8 16,12 C6,18 -6,10 -12,12 C-24,16 -28,8 -22,2 Z",
	"speck": "M-4,-1 C-6,-5 0,-7 3,-4 C6,-6 8,0 5,3 C6,6 0,7 -3,4 C-6,5 -7,1 -4,-1 Z",
	"splash": "M-6,-12 C4,-18 16,-8 12,0 C18,4 14,14 4,12 C2,20 -12,16 -14,6 C-22,4 -18,-4 -6,-12 Z",
	"drop": "M2,-18 C10,-16 14,-6 8,2 C16,10 6,20 -2,14 C-12,18 -16,6 -10,-2 C-16,-12 -8,-20 2,-18 Z",
	"pair": "M-16,-4 C-12,-14 0,-12 2,-4 C8,-14 20,-8 16,2 C22,10 8,16 0,10 C-2,16 -14,12 -16,4 C-24,2 -22,0 -16,-4 Z",
}

# Placed by eye against the leopard horses in the coat guides.
# Spots cross the neck, back, ribs, and hip. Large and small marks share a region.
# Open pale coat is left between groups. name, x, y, rotation, scale x, scale y
SPOT_PLACEMENT = (
	("speck", 178, 305, 15, 0.7, 0.55),
	("drop", 205, 345, -25, 0.65, 0.85),
	("blot", 255, 365, -18, 1.05, 0.8),
	("bean", 295, 395, 22, 0.9, 0.7),
	("speck", 235, 415, 40, 0.55, 0.45),
	("splash", 330, 375, -10, 0.85, 0.6),
	("blot", 385, 400, 12, 1.25, 0.85),
	("speck", 445, 388, -30, 0.6, 0.5),
	("peanut", 500, 405, 18, 1.0, 0.7),
	("comma", 555, 395, -35, 0.9, 1.05),
	("bean", 360, 455, -20, 1.15, 0.85),
	("drop", 425, 470, 35, 0.8, 1.1),
	("speck", 470, 440, 8, 0.5, 0.4),
	("pair", 520, 460, -12, 1.2, 0.9),
	("blot", 575, 450, 28, 1.4, 1.05),
	("splash", 610, 490, -22, 0.95, 0.75),
	("speck", 540, 500, 16, 0.65, 0.5),
	("comma", 490, 505, 48, 0.75, 0.95),
	("speck", 315, 520, -8, 0.55, 0.7),
	("drop", 590, 545, 20, 0.5, 0.65),
)

# Three separate frame regions. Blur welds each cluster and hides corners.
# Shoulder runs down the neck, the barrel patch sits lower, the hip patch sits higher.
FRAME_PATCHES = (
	"M278 448 C250 424 296 384 322 414 C348 388 346 436 326 460 C358 472 308 502 282 480 C260 494 266 462 278 448 Z",
	"M300 478 C280 512 318 534 340 512 C352 538 322 556 302 530 C286 548 284 504 300 478 Z",
	"M332 402 C320 388 350 384 354 400 C360 388 342 418 326 412 C316 416 324 410 332 402 Z",
	"M448 508 C428 492 456 476 476 496 C496 482 502 512 478 522 C490 538 448 534 438 516 C422 522 434 514 448 508 Z",
	"M468 532 C454 516 486 506 498 522 C508 538 476 548 462 534 Z",
	"M572 452 C552 432 590 416 616 442 C636 428 640 468 616 484 C632 504 590 500 574 478 C558 488 562 462 572 452 Z",
	"M604 424 C590 408 624 400 636 418 C644 404 630 444 610 438 Z",
)

# Fewspot, from the guide note on homozygous LP: a crisp white body and only a few dark spots.
FEWSPOT_PLACEMENT = (
	("speck", 250, 390, 20, 0.7, 0.55),
	("bean", 470, 450, -15, 0.75, 0.6),
	("drop", 545, 430, 25, 0.7, 0.85),
	("speck", 600, 490, -10, 0.6, 0.5),
	("comma", 330, 470, 30, 0.55, 0.7),
)

COATS = (
	{"id": "neither-modeled-pattern", "title": "Neither modeled pattern", "subtitle": "No frame and no leopard complex", "base": CHESTNUT, "spots": None, "frame": False, "x": 0, "y": 0},
	{"id": "frame-overo", "title": "Frame-overo", "subtitle": "Colored frame, white side", "base": CHESTNUT, "spots": None, "frame": True, "x": 520, "y": 0},
	{"id": "leopard-complex", "title": "Leopard-complex", "subtitle": "Pale coat, spots over the body", "base": PALE, "spots": "leopard", "frame": False, "x": 1040, "y": 0},
	{"id": "fewspot", "title": "Fewspot", "subtitle": "Mostly white, only a few spots", "base": "#fbfaf7", "spots": "few", "frame": False, "x": 260, "y": 640},
	{"id": "pintaloosa", "title": "Pintaloosa", "subtitle": "Frame patches and leopard spots", "base": CHESTNUT, "spots": "leopard", "frame": True, "x": 780, "y": 640},
)


#========================================================
def flatten_path(path_data: str) -> list:
	"""Sample one SVG path into rings. The chestnut commands are m, l, h, v, c, s, and z."""
	tokens = re.findall(r"[mlhvcsz]|-?\d+(?:\.\d+)?", path_data)
	index = 0
	command = ""
	x = y = 0.0
	start = (0.0, 0.0)
	cubic_control = (0.0, 0.0)
	rings = []
	ring = []

	def read_number():
		nonlocal index
		value = float(tokens[index])
		index += 1
		return value

	def line_to(px, py):
		nonlocal x, y
		ring.append((px, py))
		x, y = px, py

	def curve_to(c1x, c1y, c2x, c2y, px, py):
		nonlocal cubic_control
		x0, y0 = x, y
		for step in range(1, 9):
			t = step / 8
			u = 1 - t
			bx = (u * u * u * x0) + (3 * u * u * t * c1x) + (3 * u * t * t * c2x) + (t * t * t * px)
			by = (u * u * u * y0) + (3 * u * u * t * c1y) + (3 * u * t * t * c2y) + (t * t * t * py)
			ring.append((bx, by))
		cubic_control = (c2x, c2y)
		line_to(px, py)

	while index < len(tokens):
		if tokens[index].isalpha() if False else re.fullmatch(r"[mlhvcsz]", tokens[index]):
			command = tokens[index]
			index += 1
		if command == "m":
			if ring:
				rings.append(ring)
				ring = []
			x += read_number()
			y += read_number()
			start = (x, y)
			ring = [(x, y)]
			command = "l"
		elif command == "l":
			line_to(x + read_number(), y + read_number())
		elif command == "h":
			line_to(x + read_number(), y)
		elif command == "v":
			line_to(x, y + read_number())
		elif command == "c":
			c1x, c1y = x + read_number(), y + read_number()
			c2x, c2y = x + read_number(), y + read_number()
			px, py = x + read_number(), y + read_number()
			curve_to(c1x, c1y, c2x, c2y, px, py)
		elif command == "s":
			c1x = (2 * x) - cubic_control[0]
			c1y = (2 * y) - cubic_control[1]
			c2x, c2y = x + read_number(), y + read_number()
			px, py = x + read_number(), y + read_number()
			curve_to(c1x, c1y, c2x, c2y, px, py)
		elif command == "z":
			line_to(*start)
			rings.append(ring)
			ring = []
		else:
			raise ValueError(f"unsupported path command {command}")
	if ring:
		rings.append(ring)
	return rings


#========================================================
def silhouette_path(paths: list) -> str:
	"""One outer contour for every coat. Phenotype layers are masked to this shape."""
	polygons = []
	for path in paths:
		if path["region"] == "feature" or path["id"] == GEOMETRIC_MARKING:
			continue
		for ring in flatten_path(path["d"]):
			if len(ring) < 4:
				continue
			polygon = shapely.geometry.Polygon(ring).buffer(0)
			if polygon.is_empty:
				continue
			polygons.append(polygon)
	union = shapely.ops.unary_union(polygons)
	# Close hairline gaps between the original pieces, then drop the slits those gaps leave behind.
	union = union.buffer(1.2).buffer(-1.2)
	parts = list(union.geoms) if union.geom_type == "MultiPolygon" else [union]
	parts = [
		shapely.geometry.Polygon(part.exterior)
		for part in parts
		if part.area > 200
	]

	def smooth_groin_notch(coords):
		"""Round the one sharp step where the belly meets the groin."""
		def turn(a, b, c):
			v1 = (a[0] - b[0], a[1] - b[1])
			v2 = (c[0] - b[0], c[1] - b[1])
			n1 = math.hypot(*v1)
			n2 = math.hypot(*v2)
			if n1 < 1e-6 or n2 < 1e-6:
				return 180.0
			dot = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))
			return math.degrees(math.acos(dot))

		corner = None
		for index in range(1, len(coords) - 1):
			x, y = coords[index]
			if not (500 < x < 560 and 470 < y < 500):
				continue
			angle = turn(coords[index - 1], coords[index], coords[index + 1])
			if corner is None or angle < corner[0]:
				corner = (angle, index)
		if corner is None or corner[0] > 120:
			return coords
		index = corner[1]
		start = max(1, index - 8)
		end = min(len(coords) - 2, index + 6)
		p0 = coords[start]
		p1 = coords[end]
		ctrl = ((p0[0] + p1[0]) / 2 + 1.5, (p0[1] + p1[1]) / 2 + 3)
		samples = []
		for step in range(1, 8):
			t = step / 8
			u = 1 - t
			samples.append((
				u * u * p0[0] + 2 * u * t * ctrl[0] + t * t * p1[0],
				u * u * p0[1] + 2 * u * t * ctrl[1] + t * t * p1[1],
			))
		return coords[:start + 1] + samples + coords[end:]

	def ring_d(coords):
		coords = smooth_groin_notch(list(coords))
		points = [f"M{coords[0][0]:.2f} {coords[0][1]:.2f}"]
		points.extend(f"L{px:.2f} {py:.2f}" for px, py in coords[1:])
		points.append("Z")
		return " ".join(points)

	return " ".join(ring_d(part.exterior.coords) for part in parts)


#========================================================
def load_paths(svg_path: Path) -> list:
	blocks = re.findall(r"<path\b[\s\S]*?/>", svg_path.read_text())
	paths = []
	for block in blocks:
		path_id = re.search(r'id="([^"]+)"', block).group(1)
		source_fill = re.search(r"fill:(#[0-9a-fA-F]+)", block).group(1)
		path_data = re.search(r'\sd="([^"]+)"', block).group(1)
		paths.append({
			"id": path_id,
			"region": REGION_BY_FILL[source_fill],
			"d": path_data,
		})
	return paths


#========================================================
def authored_spots() -> str:
	library = "\n".join(
		f'    <symbol id="spot-{name}" overflow="visible"><path d="{path_data}"/></symbol>'
		for name, path_data in SPOT_LIBRARY.items()
	)
	def placed(rows):
		return "\n".join(
			f'      <use href="#spot-{name}" transform="translate({x} {y}) rotate({rotation}) scale({scale_x} {scale_y})"/>'
			for name, x, y, rotation, scale_x, scale_y in rows
		)
	return library, placed(SPOT_PLACEMENT), placed(FEWSPOT_PLACEMENT)


#========================================================
def use_paths(paths: list, region: str) -> str:
	return "\n        ".join(
		f'<use href="#{path["id"]}"/>'
		for path in paths
		if path["region"] == region and path["id"] != GEOMETRIC_MARKING
	)


#========================================================
def horse_stack(paths: list, coat: dict) -> str:
	coat_uses = use_paths(paths, "coat")
	sock_uses = use_paths(paths, "marking")
	frame_seeds = "\n        ".join(
		f'<path d="{path_data}"/>' for path_data in FRAME_PATCHES
	)
	layers = [
		f'<use href="#silhouette" fill="{coat["base"]}"/>',
		f'<g id="{coat["id"]}-base" fill="{coat["base"]}">\n        {coat_uses}\n      </g>',
	]
	if coat["spots"] == "leopard":
		layers.append('<use href="#leopard-spots" fill="#2a241c"/>')
	if coat["spots"] == "few":
		layers.append('<use href="#few-spots" fill="#2a241c"/>')
	if coat["frame"]:
		layers.append(
			f'<g fill="{WHITE}" filter="url(#organic-frame)">\n        {frame_seeds}\n      </g>'
		)
	layers.append(f'<g fill="{WHITE}">\n        {sock_uses}\n      </g>')
	for region in ("mane", "ear", "muzzle", "hoof", "feature"):
		layers.append(
			f'<g fill="{DETAIL_FILL[region]}">\n        {use_paths(paths, region)}\n      </g>'
		)
	painted = "\n      ".join(layers)
	return (
		f'<g mask="url(#horse-silhouette)">\n      {painted}\n      </g>\n'
		f'      <use href="#silhouette" fill="none" stroke="{STRUCTURE}" stroke-width="2.4" '
		f'stroke-linejoin="round" stroke-linecap="round"/>'
	)


#========================================================
def build_svg(paths: list) -> str:
	symbols = "\n".join(
		f'    <symbol id="{path["id"]}" overflow="visible"><path d="{path["d"]}" fill-rule="evenodd"/></symbol>'
		for path in paths
	)
	spot_symbols, leopard_uses, few_uses = authored_spots()
	outline = silhouette_path(paths)
	panels = []
	for coat in COATS:
		panels.append(
			f'''  <g id="{coat["id"]}" transform="translate({coat["x"]} {coat["y"]})">
    <rect width="500" height="620" rx="18" fill="url(#field)"/>
    <g transform="translate(22 8) scale(0.88) translate(-127.06 -200.01)">
      {horse_stack(paths, coat)}
    </g>
    <text x="250" y="582" text-anchor="middle" font-family="Palatino, Georgia, serif" font-size="26" font-weight="700" fill="#2c241c">{coat["title"]}</text>
    <text x="250" y="606" text-anchor="middle" font-family="Palatino, Georgia, serif" font-size="14" fill="#5c5146">{coat["subtitle"]}</text>
  </g>'''
		)
	return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1540 1260" role="img" aria-labelledby="title desc">
  <title id="title">Five representative horse coat patterns</title>
  <desc id="desc">One chestnut horse shown as five teaching coats. Neither modeled pattern is the plain chestnut. Frame-overo keeps a colored topline and legs around white side patches. Leopard-complex is a pale coat with spots across the body. Fewspot is mostly white with only a few dark spots. Pintaloosa combines the frame patches and the leopard spots.</desc>
  <!-- Anatomy: chestnut horse by Jan Graham, OpenClipart 259732, public domain.
       https://openclipart.org/detail/259732/chestnut-horse-for-big-read
       Each path is stored once. Coats select the base fill, the leopard spot field, and the frame marking layer. -->
  <rect width="1540" height="1260" fill="#fbf8f3"/>
  <defs>
    <linearGradient id="field" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fbf8f3"/>
      <stop offset="1" stop-color="#f0e6d8"/>
    </linearGradient>
    <filter id="organic-frame" x="-0.5" y="-0.5" width="2" height="2" color-interpolation-filters="sRGB">
      <feGaussianBlur stdDeviation="9" result="blurred"/>
      <feColorMatrix in="blurred" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 28 -12"/>
    </filter>
    <mask id="horse-silhouette" maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse" x="0" y="0" width="900" height="1000">
      <path id="silhouette-fill" d="{outline}" fill="white"/>
    </mask>
    <path id="silhouette" d="{outline}"/>
{spot_symbols}
    <g id="leopard-spots" fill="#2a241c">
{leopard_uses}
    </g>
    <g id="few-spots" fill="#2a241c">
{few_uses}
    </g>
{symbols}
  </defs>
{chr(10).join(panels)}
</svg>
'''


#========================================================
def write_figure():
	paths = load_paths(CHESTNUT_SVG)
	FIGURE_SVG.write_text(build_svg(paths))
	rsvg_convert = shutil.which("rsvg-convert")
	if rsvg_convert is None:
		raise SystemExit("rsvg-convert is required to render horse_coat_patterns.png")
	subprocess.run(
		[rsvg_convert, "-w", "1540", "-h", "1260", "-o", str(FIGURE_PNG), str(FIGURE_SVG)],
		check=True,
	)


#========================================================
def main():
	write_figure()


#========================================================
if __name__ == "__main__":
	main()
